import pkg_resources

installed_packages = sorted([f'{package.key}=={package.version}' for package in pkg_resources.working_set])

print("\nInstalled Python Packages:")
for package in installed_packages:
    print(f"- {package}")
