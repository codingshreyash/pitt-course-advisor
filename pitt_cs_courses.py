#!/usr/bin/env python3
"""
Pitt CS Courses MCP Server

This MCP server provides tools for searching and retrieving information about 
University of Pittsburgh School of Computing and Information courses.
"""

import asyncio
import json
import re
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.models import (
    CallToolRequest,
    CallToolResult,
    GetPromptRequest,
    GetPromptResult,
    ListPromptsRequest,
    ListPromptsResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    ReadResourceRequest,
    ReadResourceResult,
    Resource,
    TextContent,
    Tool,
)
from mcp.types import (
    McpError,
    ErrorCode,
)

# Base URL for the courses site
BASE_URL = "https://courses.sci.pitt.edu"
COURSES_URL = f"{BASE_URL}/courses"

class Course:
    """Represents a course with its details"""
    def __init__(self, code: str, title: str, url: str):
        self.code = code
        self.title = title
        self.url = url
        self.description = ""
        self.prerequisites = ""
        self.corequisites = ""
        self.credits_min = None
        self.credits_max = None
        self.career = ""
        self.component = ""
        self.grade_component = ""
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "prerequisites": self.prerequisites,
            "corequisites": self.corequisites,
            "credits_min": self.credits_min,
            "credits_max": self.credits_max,
            "career": self.career,
            "component": self.component,
            "grade_component": self.grade_component
        }

class PittCoursesClient:
    """Client for scraping Pitt CS courses data"""
    
    def __init__(self):
        self.courses_cache: Dict[str, Course] = {}
        self.courses_list_cache: List[Course] = []
        
    async def _fetch_page(self, url: str) -> str:
        """Fetch a webpage and return its content"""
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
            
    async def _parse_course_list(self) -> List[Course]:
        """Parse the main courses page to get all course listings"""
        html = await self._fetch_page(COURSES_URL)
        soup = BeautifulSoup(html, 'html.parser')
        
        courses = []
        # Find all course links
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and href.startswith('/courses/view/'):
                # Extract course code and title from link text
                link_text = link.get_text().strip()
                if ' ' in link_text:
                    # Format is usually "CODE TITLE"
                    parts = link_text.split(' ', 1)
                    if len(parts) >= 2:
                        code = parts[0]
                        title = parts[1]
                        full_url = urljoin(BASE_URL, href)
                        course = Course(code, title, full_url)
                        courses.append(course)
                        
        return courses
        
    async def _parse_course_details(self, course: Course) -> Course:
        """Parse individual course page for detailed information"""
        try:
            html = await self._fetch_page(course.url)
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract course description (usually in the main content area)
            desc_elem = soup.find('p') or soup.find('div', class_='description')
            if desc_elem:
                course.description = desc_elem.get_text().strip()
            
            # Extract structured course information
            text = soup.get_text()
            
            # Parse prerequisites
            preq_match = re.search(r'PREQ:\s*([^·]+)', text, re.IGNORECASE)
            if preq_match:
                course.prerequisites = preq_match.group(1).strip()
            
            # Parse corequisites  
            creq_match = re.search(r'CREQ:\s*([^·]+)', text, re.IGNORECASE)
            if creq_match:
                course.corequisites = creq_match.group(1).strip()
                
            # Parse credits
            credits_match = re.search(r'Minimum Credits:\s*(\d+).*?Maximum Credits:\s*(\d+)', text, re.DOTALL)
            if credits_match:
                course.credits_min = int(credits_match.group(1))
                course.credits_max = int(credits_match.group(2))
                
            # Parse career level
            career_match = re.search(r'Academic Career:\s*(\w+)', text)
            if career_match:
                course.career = career_match.group(1)
                
            # Parse component
            component_match = re.search(r'Course Component:\s*([^·]+)', text)
            if component_match:
                course.component = component_match.group(1).strip()
                
        except Exception as e:
            print(f"Error parsing course details for {course.code}: {e}")
            
        return course
        
    async def get_all_courses(self, refresh: bool = False) -> List[Course]:
        """Get all courses, using cache if available"""
        if not refresh and self.courses_list_cache:
            return self.courses_list_cache
            
        courses = await self._parse_course_list()
        self.courses_list_cache = courses
        
        # Update courses cache
        for course in courses:
            self.courses_cache[course.code] = course
            
        return courses
        
    async def get_course_details(self, course_code: str) -> Optional[Course]:
        """Get detailed information for a specific course"""
        course_code = course_code.upper().replace(' ', '-')
        
        # Check cache first
        if course_code in self.courses_cache:
            course = self.courses_cache[course_code]
            if course.description:  # Already has details
                return course
                
        # Find course in list
        courses = await self.get_all_courses()
        course = next((c for c in courses if c.code.replace(' ', '-') == course_code), None)
        
        if not course:
            return None
            
        # Fetch detailed information
        detailed_course = await self._parse_course_details(course)
        self.courses_cache[course_code] = detailed_course
        
        return detailed_course
        
    async def search_courses(self, query: str, department: Optional[str] = None) -> List[Course]:
        """Search courses by query string"""
        courses = await self.get_all_courses()
        query_lower = query.lower()
        results = []
        
        for course in courses:
            # Check if query matches code, title, or description
            if (query_lower in course.code.lower() or 
                query_lower in course.title.lower() or
                (course.description and query_lower in course.description.lower())):
                
                # Filter by department if specified
                if department:
                    dept_code = course.code.split('-')[0] if '-' in course.code else course.code.split(' ')[0]
                    if dept_code.upper() != department.upper():
                        continue
                        
                results.append(course)
                
        return results
        
    def parse_prerequisites(self, prereq_string: str) -> List[List[str]]:
        """Parse prerequisite string into structured format"""
        if not prereq_string:
            return []
            
        # Simple parsing - this could be made more sophisticated
        # Handle common patterns like "CS 0441 and CS 0445" or "CS 0445 or COE 0445"
        
        # Replace common course patterns
        prereq_string = re.sub(r'(\w+)\s+(\d{4})', r'\1-\2', prereq_string)
        
        # Split by major conjunctions
        or_groups = re.split(r'\s+or\s+', prereq_string, flags=re.IGNORECASE)
        
        prerequisites = []
        for group in or_groups:
            # Split by 'and' within each group
            and_courses = re.split(r'\s+and\s+', group, flags=re.IGNORECASE)
            clean_courses = []
            
            for course in and_courses:
                # Extract course codes
                course_match = re.search(r'([A-Z]+[-\s]?\d{4})', course)
                if course_match:
                    clean_courses.append(course_match.group(1))
                    
            if clean_courses:
                prerequisites.append(clean_courses)
                
        return prerequisites

# Initialize the client
client = PittCoursesClient()

# Create the server
server = Server("pitt-cs-courses")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="search_courses",
            description="Search for courses by keyword, course code, or title",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (course code, title, or keyword)"
                    },
                    "department": {
                        "type": "string",
                        "description": "Filter by department code (CS, INFSCI, CMPINF, etc.)",
                        "enum": ["CS", "INFSCI", "CMPINF", "LIS", "TELCOM", "ISSP"]
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_course_details",
            description="Get detailed information for a specific course",
            inputSchema={
                "type": "object", 
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code (e.g., 'CS-0445' or 'CS 0445')"
                    }
                },
                "required": ["course_code"]
            }
        ),
        Tool(
            name="get_prerequisites",
            description="Get prerequisite information for a course",
            inputSchema={
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string", 
                        "description": "Course code (e.g., 'CS-0445' or 'CS 0445')"
                    }
                },
                "required": ["course_code"]
            }
        ),
        Tool(
            name="list_courses_by_department",
            description="List all courses for a specific department",
            inputSchema={
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "description": "Department code",
                        "enum": ["CS", "INFSCI", "CMPINF", "LIS", "TELCOM", "ISSP"]
                    }
                },
                "required": ["department"]
            }
        ),
        Tool(
            name="find_prerequisite_chain",
            description="Find the prerequisite chain for a course (what courses you need to take before this one)",
            inputSchema={
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code (e.g., 'CS-1501' or 'CS 1501')"
                    }
                },
                "required": ["course_code"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
    """Handle tool calls"""
    
    if name == "search_courses":
        query = arguments.get("query", "")
        department = arguments.get("department")
        
        if not query:
            return CallToolResult(content=[TextContent(type="text", text="Query parameter is required")])
            
        try:
            results = await client.search_courses(query, department)
            
            if not results:
                return CallToolResult(content=[TextContent(
                    type="text", 
                    text=f"No courses found matching '{query}'" + (f" in department {department}" if department else "")
                )])
            
            # Format results
            text_results = []
            for course in results[:20]:  # Limit to 20 results
                text_results.append(f"**{course.code}**: {course.title}")
                if course.description:
                    text_results.append(f"  {course.description[:200]}{'...' if len(course.description) > 200 else ''}")
                text_results.append("")
                
            return CallToolResult(content=[TextContent(
                type="text", 
                text="\n".join(text_results)
            )])
            
        except Exception as e:
            raise McpError(ErrorCode.INTERNAL_ERROR, f"Search failed: {str(e)}")
    
    elif name == "get_course_details":
        course_code = arguments.get("course_code", "")
        
        if not course_code:
            return CallToolResult(content=[TextContent(type="text", text="Course code is required")])
            
        try:
            course = await client.get_course_details(course_code)
            
            if not course:
                return CallToolResult(content=[TextContent(
                    type="text", 
                    text=f"Course '{course_code}' not found"
                )])
                
            details = []
            details.append(f"# {course.code}: {course.title}")
            details.append("")
            
            if course.description:
                details.append(f"**Description**: {course.description}")
                details.append("")
                
            if course.prerequisites:
                details.append(f"**Prerequisites**: {course.prerequisites}")
                
            if course.corequisites:
                details.append(f"**Corequisites**: {course.corequisites}")
                
            if course.credits_min is not None:
                if course.credits_min == course.credits_max:
                    details.append(f"**Credits**: {course.credits_min}")
                else:
                    details.append(f"**Credits**: {course.credits_min}-{course.credits_max}")
                    
            if course.career:
                details.append(f"**Level**: {course.career}")
                
            if course.component:
                details.append(f"**Component**: {course.component}")
                
            details.append(f"\n**URL**: {course.url}")
            
            return CallToolResult(content=[TextContent(
                type="text", 
                text="\n".join(details)
            )])
            
        except Exception as e:
            raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to get course details: {str(e)}")
    
    elif name == "get_prerequisites":
        course_code = arguments.get("course_code", "")
        
        try:
            course = await client.get_course_details(course_code)
            
            if not course:
                return CallToolResult(content=[TextContent(
                    type="text", 
                    text=f"Course '{course_code}' not found"
                )])
                
            if not course.prerequisites:
                return CallToolResult(content=[TextContent(
                    type="text", 
                    text=f"{course.code} has no prerequisites listed"
                )])
                
            # Parse prerequisites into structured format
            parsed_prereqs = client.parse_prerequisites(course.prerequisites)
            
            result = [f"# Prerequisites for {course.code}: {course.title}"]
            result.append("")
            result.append(f"**Raw Prerequisites**: {course.prerequisites}")
            result.append("")
            
            if parsed_prereqs:
                result.append("**Structured Prerequisites**:")
                for i, group in enumerate(parsed_prereqs):
                    if len(group) == 1:
                        result.append(f"- {group[0]}")
                    else:
                        result.append(f"- {' AND '.join(group)}")
                        
            return CallToolResult(content=[TextContent(
                type="text", 
                text="\n".join(result)
            )])
            
        except Exception as e:
            raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to get prerequisites: {str(e)}")
    
    elif name == "list_courses_by_department":
        department = arguments.get("department", "")
        
        if not department:
            return CallToolResult(content=[TextContent(type="text", text="Department parameter is required")])
            
        try:
            courses = await client.get_all_courses()
            dept_courses = [c for c in courses if c.code.startswith(department)]
            
            if not dept_courses:
                return CallToolResult(content=[TextContent(
                    type="text", 
                    text=f"No courses found for department '{department}'"
                )])
                
            result = [f"# {department} Courses ({len(dept_courses)} total)"]
            result.append("")
            
            for course in dept_courses:
                result.append(f"**{course.code}**: {course.title}")
                
            return CallToolResult(content=[TextContent(
                type="text", 
                text="\n".join(result)
            )])
            
        except Exception as e:
            raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to list courses: {str(e)}")
    
    elif name == "find_prerequisite_chain":
        course_code = arguments.get("course_code", "")
        
        try:
            # This is a simplified prerequisite chain finder
            # In a full implementation, you'd recursively resolve all prerequisites
            course = await client.get_course_details(course_code)
            
            if not course:
                return CallToolResult(content=[TextContent(
                    type="text", 
                    text=f"Course '{course_code}' not found"
                )])
                
            result = [f"# Prerequisite Chain for {course.code}"]
            result.append("")
            
            if not course.prerequisites:
                result.append("This course has no prerequisites.")
                return CallToolResult(content=[TextContent(type="text", text="\n".join(result))])
                
            result.append(f"**Direct Prerequisites**: {course.prerequisites}")
            result.append("")
            result.append("**Note**: This shows direct prerequisites only. For a complete prerequisite chain, you would need to check the prerequisites of each prerequisite course recursively.")
            
            # Parse and show structured prerequisites
            parsed_prereqs = client.parse_prerequisites(course.prerequisites)
            if parsed_prereqs:
                result.append("")
                result.append("**Structured Prerequisites**:")
                for group in parsed_prereqs:
                    if len(group) == 1:
                        result.append(f"- Take: {group[0]}")
                    else:
                        result.append(f"- Take all of: {', '.join(group)}")
            
            return CallToolResult(content=[TextContent(
                type="text", 
                text="\n".join(result)
            )])
            
        except Exception as e:
            raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to find prerequisite chain: {str(e)}")
    
    else:
        raise McpError(ErrorCode.METHOD_NOT_FOUND, f"Unknown tool: {name}")

async def main():
    # Import here to avoid issues with event loops
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pitt-cs-courses",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
