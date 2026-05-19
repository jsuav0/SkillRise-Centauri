"""
centauri.py — Centauri Data Explorer
Reads and displays events, tech hubs, and course data from the Centauri platform.

Requirements:
    pip install rich

Usage:
    python centauri.py
"""

import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich import box
from rich.prompt import Prompt, IntPrompt
from rich.rule import Rule

console = Console()

# ──────────────────────────────────────────────
# DATA
# ──────────────────────────────────────────────

EVENTS = [
    {
        "id": "london-web",
        "name": "Web Dev Bootcamp",
        "city": "London",
        "date": "Sat 14 June 2026",
        "time": "11:00 – 15:00",
        "location": "Tower Hamlets Community Hub",
        "description": "A friendly intro to building your first website. No experience needed — just curiosity. We'll cover HTML, CSS and how to put your work online.",
        "skills": ["HTML", "CSS", "Coding Basics", "Teamwork"],
        "has_devices": True,
    },
    {
        "id": "birmingham-cv",
        "name": "CV & Career Day",
        "city": "Birmingham",
        "date": "Sun 22 June 2026",
        "time": "12:00 – 16:00",
        "location": "Digbeth Youth Centre",
        "description": "Build a CV that actually gets read. Mock interviews, LinkedIn tips, and a chat with people working in tech today.",
        "skills": ["CV Writing", "Interviews", "LinkedIn"],
        "has_devices": True,
    },
    {
        "id": "manchester-excel",
        "name": "Excel for Real Life",
        "city": "Manchester",
        "date": "Sat 5 July 2026",
        "time": "10:00 – 13:00",
        "location": "Moss Side Library",
        "description": "Learn the spreadsheet skills employers actually ask for. Budgets, charts, formulas — explained simply.",
        "skills": ["Excel", "Data Basics", "Problem Solving"],
        "has_devices": False,
    },
    {
        "id": "leeds-ai",
        "name": "Intro to AI Tools",
        "city": "Leeds",
        "date": "Wed 16 July 2026",
        "time": "17:30 – 20:00",
        "location": "Chapeltown Tech Space",
        "description": "What is AI, really? Hands-on play with the tools changing how we work, study and create.",
        "skills": ["AI Basics", "Prompting", "Critical Thinking"],
        "has_devices": True,
    },
    {
        "id": "glasgow-code",
        "name": "Code Your First App",
        "city": "Glasgow",
        "date": "Sat 26 July 2026",
        "time": "11:00 – 15:00",
        "location": "Govan Youth Hub",
        "description": "Build a small phone app from scratch and walk out having shipped something real.",
        "skills": ["Coding Basics", "Mobile", "Creativity"],
        "has_devices": False,
    },
    {
        "id": "cardiff-design",
        "name": "Design with Figma",
        "city": "Cardiff",
        "date": "Sun 3 August 2026",
        "time": "13:00 – 16:00",
        "location": "Butetown Community Centre",
        "description": "Learn the design tool used at companies like Google and the BBC. Make a poster, an app screen and a portfolio piece.",
        "skills": ["Figma", "Design", "Portfolio"],
        "has_devices": True,
    },
]

COURSES = [
    {"id": "creative-design",    "title": "Creative Design",      "difficulty": "Beginner",     "duration": "4 Weeks", "xp": 1500, "description": "Master visual communication, layout, and digital branding."},
    {"id": "ai-fundamentals",    "title": "AI Fundamentals",      "difficulty": "Beginner",     "duration": "3 Weeks", "xp": 1200, "description": "Learn what AI is, how it learns, and how to use it responsibly."},
    {"id": "digital-marketing",  "title": "Digital Marketing",    "difficulty": "Beginner",     "duration": "4 Weeks", "xp": 1300, "description": "Grow an audience and turn engagement into real-world opportunity."},
    {"id": "video-content",      "title": "Video & Content",      "difficulty": "Beginner",     "duration": "3 Weeks", "xp": 1100, "description": "Plan, shoot, and edit videos that tell your story."},
    {"id": "web-development",    "title": "Web Development",      "difficulty": "Intermediate", "duration": "6 Weeks", "xp": 2000, "description": "Build and deploy your first real website from scratch."},
    {"id": "coding-starter",     "title": "Coding Starter",       "difficulty": "Beginner",     "duration": "4 Weeks", "xp": 1400, "description": "Write your first lines of code and learn how computers think."},
]

# Hubs are loaded from hubs.json if present, otherwise a sample is used
def load_hubs():
    try:
        with open("hubs.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback sample
        return [
            {"name": "ONE Tech Hub",            "city": "Aberdeen",   "postcode": "AB10 1JQ", "type": "Technology Hub",           "region": "Scotland",        "nation": "Scotland",       "category": "Regional tech hub"},
            {"name": "CodeBase Edinburgh",       "city": "Edinburgh",  "postcode": "EH1 2EL",  "type": "Technology Hub",           "region": "Scotland",        "nation": "Scotland",       "category": "Technology incubator"},
            {"name": "Campus London",            "city": "London",     "postcode": "E1W 1YW",  "type": "Innovation Hub",           "region": "London",          "nation": "England",        "category": "Google for Startups"},
            {"name": "Manchester Science Park",  "city": "Manchester", "postcode": "M15 6SZ",  "type": "Science Park",             "region": "North West",      "nation": "England",        "category": "UKSPA member"},
            {"name": "Bruntwood SciTech",        "city": "Birmingham", "postcode": "B7 4BB",   "type": "Innovation District",      "region": "West Midlands",   "nation": "England",        "category": "Innovation district"},
            {"name": "TechHub Cardiff",          "city": "Cardiff",    "postcode": "CF10 1EP", "type": "Technology Hub",           "region": "Wales",           "nation": "Wales",          "category": "Regional tech hub"},
        ]

# ──────────────────────────────────────────────
# DISPLAY FUNCTIONS
# ──────────────────────────────────────────────

def show_banner():
    console.print()
    console.print(Panel.fit(
        "[bold cyan]★  CENTAURI  ★[/bold cyan]\n[dim]UK Youth Digital Platform — Data Explorer[/dim]",
        border_style="cyan",
        padding=(1, 4),
    ))
    console.print()

def show_menu():
    console.print("[bold white]What would you like to explore?[/bold white]\n")
    options = [
        ("1", "📅  Upcoming Events",     "cyan"),
        ("2", "🏢  UK Tech Hubs",        "cyan"),
        ("3", "🎓  Learning Courses",    "cyan"),
        ("4", "🔍  Search Hubs by City", "cyan"),
        ("5", "📊  Hubs by Region",      "cyan"),
        ("0", "Exit",                    "dim"),
    ]
    for key, label, style in options:
        console.print(f"  [{style}]{key}[/{style}]  {label}")
    console.print()


def show_events():
    console.print(Rule("[bold cyan]Upcoming Events[/bold cyan]"))
    console.print()

    table = Table(
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold cyan",
        show_lines=True,
    )
    table.add_column("#",           style="dim",        width=3)
    table.add_column("Event",       style="bold white", min_width=22)
    table.add_column("City",        style="cyan",       width=12)
    table.add_column("Date",        style="green",      min_width=18)
    table.add_column("Time",        style="yellow",     width=14)
    table.add_column("Skills",      style="white",      min_width=28)
    table.add_column("Devices",     style="green",      width=8)

    for i, e in enumerate(EVENTS, 1):
        skills_str = ", ".join(e["skills"])
        devices = "✓" if e["has_devices"] else "—"
        table.add_row(str(i), e["name"], e["city"], e["date"], e["time"], skills_str, devices)

    console.print(table)
    console.print()

    # Ask if they want event detail
    choice = Prompt.ask(
        "Enter event number for details, or press [bold]Enter[/bold] to go back",
        default=""
    )
    if choice.isdigit() and 1 <= int(choice) <= len(EVENTS):
        show_event_detail(EVENTS[int(choice) - 1])


def show_event_detail(event):
    console.print()
    console.print(Panel(
        f"[bold cyan]{event['city'].upper()}[/bold cyan]\n"
        f"[bold white]{event['name']}[/bold white]\n\n"
        f"[yellow]📅  {event['date']}  ·  {event['time']}[/yellow]\n"
        f"[dim]📍  {event['location']}[/dim]\n\n"
        f"{event['description']}\n\n"
        f"[bold]Skills:[/bold] [cyan]{', '.join(event['skills'])}[/cyan]\n"
        f"[bold]Devices provided:[/bold] {'[green]Yes ✓[/green]' if event['has_devices'] else '[dim]No[/dim]'}",
        title="[bold]Event Detail[/bold]",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print()
    Prompt.ask("Press [bold]Enter[/bold] to continue", default="")


def show_hubs(hubs=None, title="UK Tech Hubs"):
    if hubs is None:
        hubs = load_hubs()

    console.print(Rule(f"[bold cyan]{title}[/bold cyan]"))
    console.print(f"  [dim]{len(hubs)} hub(s) found[/dim]\n")

    table = Table(
        box=box.SIMPLE_HEAVY,
        border_style="cyan",
        header_style="bold cyan",
        show_lines=False,
    )
    table.add_column("#",          style="dim",        width=4)
    table.add_column("Hub Name",   style="bold white", min_width=32)
    table.add_column("City",       style="cyan",       width=14)
    table.add_column("Postcode",   style="yellow",     width=10)
    table.add_column("Type",       style="white",      min_width=22)
    table.add_column("Region",     style="green",      min_width=18)

    for i, h in enumerate(hubs[:50], 1):  # cap at 50 for readability
        table.add_row(str(i), h["name"], h["city"], h["postcode"], h["type"], h["region"])

    console.print(table)

    if len(hubs) > 50:
        console.print(f"  [dim]... and {len(hubs) - 50} more. Use Search or Region filter to narrow down.[/dim]")
    console.print()
    Prompt.ask("Press [bold]Enter[/bold] to continue", default="")


def search_hubs_by_city():
    console.print(Rule("[bold cyan]Search Hubs by City[/bold cyan]"))
    query = Prompt.ask("\n  Enter city or postcode").strip().lower()

    if not query:
        return

    hubs = load_hubs()
    results = [
        h for h in hubs
        if query in h["city"].lower()
        or query in h["postcode"].lower()
        or query in h["name"].lower()
    ]

    if results:
        show_hubs(results, title=f'Results for "{query}"')
    else:
        console.print(f"\n  [yellow]No hubs found matching '{query}'.[/yellow]\n")
        Prompt.ask("Press [bold]Enter[/bold] to continue", default="")


def show_hubs_by_region():
    hubs = load_hubs()
    regions = sorted(set(h["region"] for h in hubs))

    console.print(Rule("[bold cyan]Hubs by Region[/bold cyan]"))
    console.print()

    # Summary table
    table = Table(box=box.SIMPLE, border_style="cyan", header_style="bold cyan")
    table.add_column("#",       style="dim",   width=4)
    table.add_column("Region",  style="white", min_width=28)
    table.add_column("Hubs",    style="cyan",  width=8, justify="right")

    for i, region in enumerate(regions, 1):
        count = sum(1 for h in hubs if h["region"] == region)
        table.add_row(str(i), region, str(count))

    console.print(table)
    console.print()

    choice = Prompt.ask(
        "Enter region number to view hubs, or press [bold]Enter[/bold] to go back",
        default=""
    )
    if choice.isdigit() and 1 <= int(choice) <= len(regions):
        region = regions[int(choice) - 1]
        filtered = [h for h in hubs if h["region"] == region]
        show_hubs(filtered, title=f"{region} Hubs")


def show_courses():
    console.print(Rule("[bold cyan]Learning Courses[/bold cyan]"))
    console.print()

    table = Table(
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold cyan",
        show_lines=True,
    )
    table.add_column("#",           style="dim",        width=3)
    table.add_column("Course",      style="bold white", min_width=22)
    table.add_column("Level",       style="cyan",       width=14)
    table.add_column("Duration",    style="yellow",     width=10)
    table.add_column("XP Reward",   style="green",      width=10, justify="right")
    table.add_column("About",       style="dim",        min_width=40)

    for i, c in enumerate(COURSES, 1):
        table.add_row(
            str(i),
            c["title"],
            c["difficulty"],
            c["duration"],
            f"{c['xp']:,} XP",
            c["description"],
        )

    console.print(table)
    console.print()
    Prompt.ask("Press [bold]Enter[/bold] to continue", default="")


# ──────────────────────────────────────────────
# MAIN LOOP
# ──────────────────────────────────────────────

def main():
    show_banner()

    while True:
        show_menu()
        choice = Prompt.ask("[bold cyan]>[/bold cyan]", default="0").strip()

        if choice == "1":
            show_events()
        elif choice == "2":
            show_hubs()
        elif choice == "3":
            show_courses()
        elif choice == "4":
            search_hubs_by_city()
        elif choice == "5":
            show_hubs_by_region()
        elif choice == "0":
            console.print("\n[bold cyan]See you around the grid. ★[/bold cyan]\n")
            break
        else:
            console.print("[yellow]  Invalid choice — pick a number from the menu.[/yellow]\n")


if __name__ == "__main__":
    main()
