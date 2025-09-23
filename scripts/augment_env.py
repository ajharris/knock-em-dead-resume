import os
import re

def fix_database_url_env(env_path: str = ".env"):
    """
    Update DATABASE_URL in the .env file to use 'postgresql://' instead of 'postgres://'.
    Only updates if necessary.
    """
    if not os.path.exists(env_path):
        print(f"No .env file found at {env_path}")
        return False
    with open(env_path, "r") as f:
        lines = f.readlines()
    changed = False
    new_lines = []
    for line in lines:
        if line.startswith("DATABASE_URL="):
            url = line[len("DATABASE_URL="):].strip()
            if url.startswith("postgres://"):
                url = "postgresql://" + url[len("postgres://"):]
                new_lines.append(f"DATABASE_URL={url}\n")
                changed = True
                print(f"Updated DATABASE_URL to use postgresql:// scheme.")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    if changed:
        with open(env_path, "w") as f:
            f.writelines(new_lines)
        print(f".env updated.")
    else:
        print(f"No change needed.")
    return changed

if __name__ == "__main__":
    fix_database_url_env()