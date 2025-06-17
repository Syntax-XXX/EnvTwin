def generate_setup_script(snapshot):
    lines = ["#!/bin/bash", "set -e"]
    os_info = snapshot['os']
    packages = snapshot['packages']
    editors = snapshot['editors']
    dbs = snapshot['databases']
    env_vars = snapshot.get('env_vars', {})
    shell_configs = snapshot.get('shell_configs', {})

    # Update and install apt packages
    lines.append("sudo apt-get update")
    apt_packages = editors + dbs
    if packages['apt']:
        for line in packages['apt']:
            if '/' in line:
                pkg = line.split('/')[0]
                if pkg not in apt_packages:
                    apt_packages.append(pkg)
    if apt_packages:
        lines.append(f"sudo apt-get install -y {' '.join(apt_packages)}")
    lines.append("sudo apt-get install -y python3-pip")

    # Install pip packages
    if packages['pip']:
        lines.append(f"pip3 install {' '.join([pkg.split('==')[0] for pkg in packages['pip']])}")

    # Install npm packages
    if packages.get('npm'):
        npm_pkgs = list(packages['npm'].keys())
        if npm_pkgs:
            lines.append(f"npm install -g {' '.join(npm_pkgs)}")

    # Set environment variables
    for k, v in env_vars.items():
        lines.append(f'export {k}="{v}"')

    # Write shell configs (as comments for manual review)
    for fname, content in shell_configs.items():
        lines.append(f"# --- {fname} ---\n# {content.replace(chr(10), chr(10)+'# ')}")

    return '\n'.join(lines)
