import os

# Mapping of programming languages to their typical file extensions
language_extensions = {
    "python": [".py"],
    "javascript": [".js", ".jsx"],
    "java": [".java"],
    "c++": [".cpp", ".hpp", ".h"],
    "c": [".c", ".h"],
    "typescript": [".ts", ".tsx"],
    "html": [".html", ".htm"],
    "css": [".css"],
    "go": [".go"],
    "ruby": [".rb"],
    "php": [".php"],
    "swift": [".swift"],
}

# Emoji assignments based on file types
file_type_emoji = {
    ".py": "🐍",        # Python files
    ".js": "📜",        # JavaScript files
    ".jsx": "⚛️",      # React JSX files
    ".java": "☕",      # Java files
    ".cpp": "➕",       # C++ files
    ".c": "🔧",         # C files
    ".ts": "🌀",        # TypeScript files
    ".tsx": "🌊",       # TypeScript React files
    ".html": "🌐",      # HTML files
    ".css": "🎨",       # CSS files
    ".go": "🐹",        # Go files (gopher)
    ".rb": "💎",        # Ruby files
    ".php": "🐘",       # PHP files (elephant)
    ".swift": "🦅",     # Swift files
}

def get_file_emoji(file_name):
    """Return the appropriate emoji for a given file based on its extension."""
    _, ext = os.path.splitext(file_name)
    return file_type_emoji.get(ext, "📄")  # Default to 📄 if no specific emoji is found

def generate_md_structure(folder_path, extensions, prefix="", include_hidden=False):
    """Recursively generate a nicely formatted markdown structure of a folder."""
    items = sorted(os.listdir(folder_path))  # Sort items for consistent order
    md_content = ""
    structure = []
    num_items = len(items)

    for i, item in enumerate(items):
        item_path = os.path.join(folder_path, item)
        is_last = i == num_items - 1  # Check if this is the last item

        # Use appropriate branch characters based on position
        branch = "└── " if is_last else "├── "
        folder_prefix = "    " if is_last else "│   "

        # Check if the item is hidden
        is_hidden = item.startswith(".")
        
        # Skip hidden directories if not including them
        if is_hidden and os.path.isdir(item_path) and not include_hidden:
            md_content += f"{prefix}{branch}~~📂 {item}~~\n"  # Mark as ignored
            continue
        
        # Skip target directory for Java projects
        if item == "target":
            md_content += f"{prefix}{branch}~~📂 {item}~~\n"  # Mark as ignored
            continue

        if os.path.isdir(item_path):
            # Add folder with 📂 emoji
            md_content += f"{prefix}{branch}📂 {item}\n"
            # Recurse into the folder with updated prefix
            sub_structure, sub_files = generate_md_structure(item_path, extensions, prefix + folder_prefix, include_hidden)
            md_content += sub_structure
            structure.extend(sub_files)  # Collect files from subdirectories
        elif os.path.isfile(item_path) and any(item.endswith(ext) for ext in extensions):
            # Add file with appropriate emoji
            file_emoji = get_file_emoji(item)
            md_content += f"{prefix}{branch}{file_emoji} {item}\n"
            # Store the file path for later content retrieval
            structure.append(item_path)
    
    return md_content, structure

def write_file_structure(language):
    """Write the file structure to the markdown file."""
    extensions = language_extensions.get(language)

    if not extensions:
        print(f"Unsupported language: {language}")
        return []

    # Start generating the markdown structure
    md_structure = "# File Structure\n\n"  # Title for the markdown
    md_structure += "```bash\n"  # Start of code block
    md_structure += f"📦 {os.path.basename(os.getcwd())}\n"
    
    structure, file_paths = generate_md_structure(os.getcwd(), extensions)
    md_structure += structure  # Add the generated structure
    md_structure += "```\n\n"  # End of the file structure code block

    # Write the structure to a markdown file, overwriting previous contents
    with open("folder_structure.md", "w") as f:
        f.write(md_structure)

    return file_paths

def write_file_contents(file_paths):
    """Append the contents of each file to the markdown file."""
    with open("folder_structure.md", "a") as f:  # Open the file in append mode
        for item_path in file_paths:
            if os.path.isfile(item_path):  # Ensure it is a file
                file_name = os.path.basename(item_path)
                f.write(f"\n📦 {os.path.basename(os.getcwd())}/📜 {file_name}\n\n")
                f.write("```" + ("js" if file_name.endswith(('.js', '.jsx')) else "txt") + "\n")  # Set language for code block
                f.write(read_file_content(item_path))  # Read file content
                f.write("```\n\n")  # Close code block

def read_file_content(file_path):
    """Read and return the contents of the file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # Optionally truncate content to first 50 lines for readability
            lines = content.splitlines()[:50]
            return "\n".join(lines) + "\n"  # Add a newline at the end
    except Exception as e:
        return f"Error reading file: {e}\n"

def main():
    # Get the programming language from the user
    language = input("Enter the programming language: ").strip().lower()
    
    # Step 1: Write the file structure to the markdown file
    file_paths = write_file_structure(language)

    # Step 2: Write the contents of each file
    write_file_contents(file_paths)

    print("Markdown structure and file contents saved to folder_structure.md")

if __name__ == "__main__":
    main()
