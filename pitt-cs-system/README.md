# 🎓 Pitt CS Course Advisor - MCP Server

A **Model Context Protocol (MCP) server** that acts as an intelligent middleman between official Pitt/SCI documentation and the student wiki, ensuring course information stays automatically updated and accessible through Claude AI.

## 🚀 What This Does

**Problem**: The existing student wiki is fantastic but static - created by students in the past, it becomes outdated as courses, prerequisites, and requirements change over time.

**Solution**: An MCP server that:
- 🔄 **Automatically syncs** with official Pitt and SCI documentation 
- 📚 **Keeps the wiki current** without manual student updates
- 🤖 **Provides AI-powered** course advisory through Claude
- ⚡ **Runs on a schedule** (cron jobs) to ensure data freshness

**Ask Claude natural questions like:**
- *"What's the current path to graduate with an AI focus?"*
- *"Has CS 1675 changed its prerequisites recently?"*
- *"What are the latest course offerings for Spring 2024?"*
- *"Find me courses that satisfy the ethics requirement"*

## 🏗️ Architecture Overview

The **MCP server acts as the intelligent middleman** that keeps the student wiki current by continuously syncing with official sources:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ OFFICIAL SOURCES│    │   MCP SERVER    │    │  STUDENT WIKI   │
│                 │    │  (MIDDLEMAN)    │    │                 │
│ • Pitt Course   │────┤ • Auto sync     │───▶│ • Always current│
│   Catalog       │    │ • Data merger   │    │ • Student tips  │
│ • SCI Docs      │    │ • Conflict res  │    │ • Community     │
│ • Requirements  │    │ • Cron jobs     │    │   insights      │
└─────────────────┘    │ • Claude AI     │    └─────────────────┘
                       └─────────────────┘            
                              │                       
                              ▼                       
                    ┌─────────────────┐               
                    │     STUDENTS    │               
                    │                 │               
                    │ Ask Claude:     │               
                    │ • Course advice │               
                    │ • Requirements  │               
                    │ • Prerequisites │               
                    └─────────────────┘               
```

### How It Works
1. **🔄 Automated Sync**: Cron jobs regularly pull latest data from official Pitt/SCI sources
2. **🤝 Smart Merging**: MCP server intelligently combines official data with existing wiki content
3. **📚 Wiki Updates**: Student wiki stays current without manual intervention
4. **🤖 AI Interface**: Students interact with always-fresh data through Claude
5. **🎯 Best of Both**: Official accuracy + community insights, automatically maintained

## 🛠️ Tech Stack

- **Backend**: Python 3.11+
- **Database**: SQLite (simple, fast, no server needed)
- **Web Scraping**: httpx + BeautifulSoup4
- **AI Interface**: MCP (Model Context Protocol)
- **Scheduling**: Cron jobs for automated updates
- **Deployment**: Single VPS/server setup

## 📁 Project Structure

```
pitt-cs-system/
├── backend/
│   ├── scrapers/
│   │   ├── wiki_scraper.py          # pittcs.wiki scraper
│   │   ├── official_scraper.py      # courses.sci.pitt.edu scraper
│   │   └── data_reconciler.py       # Smart data merging
│   ├── database/
│   │   ├── models.py               # Database schema
│   │   ├── courses_db.py           # Database operations
│   │   └── pitt_courses.db         # SQLite database
│   ├── api/
│   │   └── mcp_server.py           # Claude MCP interface
│   ├── cron/
│   │   ├── update_schedule.py      # Automated data updates
│   │   └── monitor.py              # Health checks
│   ├── shared/
│   │   ├── config.py               # Configuration
│   │   └── utils.py                # Common utilities
│   └── requirements.txt
├── config/
│   ├── claude_desktop_config.json  # MCP configuration
│   └── crontab                     # Cron schedule
├── logs/                           # Application logs
├── tests/                          # Unit tests
└── README.md
```

## ⚡ Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/pitt-cs-system
cd pitt-cs-system
pip install -r backend/requirements.txt
```

### 2. Initialize Database
```bash
cd backend
python -c "from database.courses_db import CoursesDatabase; CoursesDatabase()"
```

### 3. Run Initial Data Scrape
```bash
python scrapers/wiki_scraper.py
python scrapers/official_scraper.py
python scrapers/data_reconciler.py
```

### 4. Configure Claude Desktop
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "pitt-cs-courses": {
      "command": "python",
      "args": ["/full/path/to/pitt-cs-system/backend/api/mcp_server.py"]
    }
  }
}
```

### 5. Test with Claude
Restart Claude Desktop and ask:
```
Search for machine learning courses at Pitt
What are the prerequisites for CS 1675?
Help me plan a path to graduate with an AI focus
```

## 🔄 Automated Updates

The system automatically updates course data:

### **Every 6 Hours**: Quick Wiki Updates
- Checks for recent changes on pittcs.wiki
- Updates only modified courses
- Fast incremental updates

### **Daily**: Full Official Site Scrape  
- Complete scan of courses.sci.pitt.edu
- Updates enrollment, schedules, official prerequisites
- Full database refresh

### **Weekly**: Data Quality Audit
- Identifies conflicts between sources
- Generates reports on data quality
- Alerts for manual review needed

## 🎯 Key Features

### **🔄 Always-Current Data (The Main Innovation)**
- **No more outdated wikis**: MCP server continuously syncs with official sources
- **Set-and-forget updates**: Cron jobs ensure data freshness without manual work
- **Future-proof**: As Pitt changes courses/requirements, the system automatically adapts
- **Zero maintenance burden**: Students always get current information

### **🤝 Smart Data Reconciliation**
- **Official data** wins for: course codes, credits, enrollment, requirements
- **Wiki data** wins for: descriptions, difficulty ratings, student tips
- **Smart merge** for: prerequisites (combines both sources intelligently)
- **Conflict detection**: Alerts when sources disagree for manual review

### **🤖 Natural Language Queries via Claude**
Students can ask conversational questions:
- "What's the current workload like for CS 1666?"
- "Show me all courses with no prerequisites this semester"
- "Which AI courses can I take after CS 1675?"
- "Have the CS degree requirements changed recently?"

### **🔗 Prerequisite Chain Analysis**
- Automatically maps prerequisite relationships
- Shows full prerequisite trees with current requirements
- Identifies circular dependencies
- Suggests optimal course sequences for graduation

### **📚 Dynamic Wiki Enhancement**
- Preserves valuable student insights and reviews
- Adds fresh official data without losing community knowledge
- Maintains difficulty ratings and professor recommendations
- Combines institutional accuracy with student experience

## 📊 Database Schema

### Core Tables
- **courses**: Main course information
- **course_sources**: Tracks data sources per field
- **data_conflicts**: Records when sources disagree
- **scrape_metadata**: Tracks update history
- **prerequisite_relationships**: Maps course dependencies

### Example Course Record
```json
{
  "code": "CS-1675",
  "title": "Introduction to Machine Learning",
  "description": "Mathematical foundations and algorithms...",
  "prerequisites": "CS 0441 and CS 0445 and (MATH 0220 or MATH 0230)",
  "credits_min": 3,
  "credits_max": 3,
  "wiki_difficulty_rating": 7.5,
  "wiki_reviews": "Challenging but rewarding. Take with Prof. Smith if possible...",
  "last_updated": "2024-01-15T10:30:00Z",
  "sources": {
    "description": "wiki",
    "prerequisites": "official", 
    "difficulty_rating": "wiki"
  }
}
```

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_PATH=backend/database/pitt_courses.db

# Scraping
WIKI_BASE_URL=https://pittcs.wiki
OFFICIAL_BASE_URL=https://courses.sci.pitt.edu

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/pitt_cs_system.log

# MCP Server
MCP_SERVER_NAME=pitt-cs-courses
MCP_SERVER_VERSION=1.0.0
```

### Cron Schedule
```bash
# Update wiki data every 6 hours
0 */6 * * * cd /path/to/project && python backend/scrapers/wiki_scraper.py

# Full official site scrape daily at 2 AM
0 2 * * * cd /path/to/project && python backend/scrapers/official_scraper.py

# Data reconciliation after updates
30 2 * * * cd /path/to/project && python backend/scrapers/data_reconciler.py

# Weekly data quality report
0 8 * * 0 cd /path/to/project && python backend/cron/quality_report.py
```

## 🚀 Deployment

### Single Server Setup (Recommended)
```bash
# 1. Clone repository
git clone https://github.com/yourusername/pitt-cs-system
cd pitt-cs-system

# 2. Install dependencies  
pip install -r backend/requirements.txt

# 3. Initialize database and run first scrape
python backend/database/init_db.py
python backend/cron/initial_scrape.py

# 4. Set up cron jobs
crontab config/crontab

# 5. Configure Claude Desktop
# Copy config/claude_desktop_config.json to appropriate location

# 6. Start monitoring (optional)
python backend/cron/monitor.py &
```

### Docker Setup (Alternative)
```bash
# Build and run
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## 🧪 Testing

### Unit Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Integration Test
```bash
# Test full scraping pipeline
python tests/test_integration.py

# Test MCP server
python tests/test_mcp_server.py
```

### Manual Testing with Claude
1. Start the MCP server: `python backend/api/mcp_server.py`
2. Open Claude Desktop
3. Try these example queries:
   - "Search for courses about databases"
   - "What are the prerequisites for CS 1980?"
   - "Show me easy CS electives"
   - "Help me plan my senior year courses"

## 📈 Monitoring

### Health Checks
- Database connectivity
- Last successful scrape timestamp
- MCP server responsiveness
- Data quality metrics

### Logs
- `logs/scraper.log`: Data collection activities
- `logs/mcp_server.log`: Claude interaction logs  
- `logs/conflicts.log`: Data source conflicts
- `logs/system.log`: General system events

### Alerts
- Data scraping failures
- Database connection issues
- High conflict rates between data sources
- MCP server downtime

## 🤝 Contributing

### Adding New Data Sources
1. Create scraper in `backend/scrapers/`
2. Add data source to reconciler
3. Update database schema if needed
4. Add tests

### Adding New MCP Tools
1. Implement tool in `backend/api/mcp_server.py`
2. Add to `@server.list_tools()` 
3. Handle in `@server.call_tool()`
4. Test with Claude

### Data Quality Improvements
- Enhance prerequisite parsing in `scrapers/prerequisite_parser.py`
- Improve conflict resolution in `scrapers/data_reconciler.py`
- Add new data validation rules

## 🐛 Troubleshooting

### Common Issues

**MCP Server Not Found in Claude**
- Check `claude_desktop_config.json` path is correct
- Ensure Python script is executable: `chmod +x backend/api/mcp_server.py`
- Restart Claude Desktop after config changes

**Database Errors**
- Check database file exists: `ls -la backend/database/pitt_courses.db`
- Verify permissions: `chmod 664 backend/database/pitt_courses.db`
- Check disk space: `df -h`

**Scraping Failures**
- Check network connectivity
- Verify source websites are accessible
- Look for rate limiting (429 errors)
- Check logs: `tail -f logs/scraper.log`

**Data Conflicts**
- Review conflict log: `tail -f logs/conflicts.log`
- Manual resolution: `python backend/tools/resolve_conflicts.py`
- Adjust reconciliation rules in `data_reconciler.py`

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
python backend/api/mcp_server.py --debug

# Check all system health
python backend/tools/health_check.py
```

## 📋 Roadmap

### Phase 1 ✅ (Current)
- [x] Basic wiki + official site scraping
- [x] SQLite database with conflict tracking  
- [x] MCP server for Claude integration
- [x] Automated updates via cron

### Phase 2 🚧 (In Progress)
- [ ] Enhanced prerequisite chain analysis
- [ ] Course difficulty predictions
- [ ] Degree planning tools
- [ ] Student review sentiment analysis

### Phase 3 📋 (Planned)
- [ ] Grade distribution integration
- [ ] Professor rating integration
- [ ] Schedule conflict detection
- [ ] Mobile app interface
- [ ] Discord/Slack bots

### Phase 4 🔮 (Future)
- [ ] Course recommendation engine
- [ ] Graduation timeline optimization
- [ ] Integration with PeopleSoft
- [ ] Multi-university support

## 📄 License

MIT License - see [LICENSE.md](LICENSE.md) for details

## 🙋‍♂️ Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/pitt-cs-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/pitt-cs-system/discussions)  
- **Email**: your.email@pitt.edu

## 🏆 Acknowledgments

- **Pitt CS Community**: For maintaining the comprehensive student wiki
- **University of Pittsburgh**: For providing official course data
- **Anthropic**: For the MCP protocol that makes AI integration seamless
- **Contributors**: See [CONTRIBUTORS.md](CONTRIBUTORS.md)

---

**Made with ❤️ for Pitt CS students**

*"Turning scattered course information into intelligent academic advice"*
