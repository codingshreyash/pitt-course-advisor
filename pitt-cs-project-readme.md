# 🎓 Pitt CS Course Data System

An intelligent course information system for University of Pittsburgh Computer Science students that combines official course data with community-driven insights from the student wiki.

## 🚀 What This Does

**Problem**: Students struggle to navigate the CS curriculum because course information is scattered across:
- Official course catalogs (often outdated)
- Student wiki (up-to-date but unstructured)  
- Word-of-mouth recommendations
- Prerequisites buried in complex text

**Solution**: An AI-powered course advisor that you can ask natural questions like:
- *"What's the easiest path to graduate with an AI focus?"*
- *"Is CS 1675 harder than CS 1501?"*
- *"What prerequisites do I need for CS 1980?"*
- *"Find me machine learning courses that aren't math-heavy"*

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   DATA SOURCES  │    │    BACKEND      │    │   AI INTERFACE  │
│                 │    │                 │    │                 │
│ • pittcs.wiki   │───▶│ • Smart merger  │───▶│ • Claude MCP    │
│ • courses.sci.  │    │ • SQLite DB     │    │ • Natural lang  │
│   pitt.edu      │    │ • Cron updates  │    │ • Conversation  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow
1. **Scrapers** pull data from official site + student wiki every 6 hours
2. **Smart merger** resolves conflicts (wiki wins for tips, official wins for requirements)
3. **Database** stores unified course information with conflict tracking
4. **MCP Server** provides conversational interface to Claude
5. **Students** ask Claude natural language questions about courses

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

### **Smart Data Reconciliation**
- **Official data** wins for: course codes, credits, enrollment
- **Wiki data** wins for: descriptions, difficulty ratings, tips
- **Smart merge** for: prerequisites (combines both sources)
- **Conflict detection** when sources disagree

### **Natural Language Queries**
Students can ask conversational questions:
- "What's the workload like for CS 1666?"
- "Show me all courses with no prerequisites"
- "Which AI courses can I take after CS 1675?"
- "What's the difference between CS 1501 and CS 1502?"

### **Prerequisite Chain Analysis**
- Automatically maps prerequisite relationships
- Shows full prerequisite trees
- Identifies circular dependencies
- Suggests course sequences

### **Student Wiki Integration**
- Real-time updates from pittcs.wiki
- Student reviews and difficulty ratings
- Professor recommendations
- Course tips and insights

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