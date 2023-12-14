import os
import shutil

class InMemoryFileSystem:
    def __init__(self):
        self.root = {'/': {}}
        self.current_directory = self.root

    def mkdir(self, path):
        if path.startswith('/'):
            directories = path.split('/')[1:]
        else:
            directories = path.split('/')

        current_dir = self.current_directory
        for directory in directories:
            if directory not in current_dir:
                current_dir[directory] = {}
            current_dir = current_dir[directory]

    def cd(self, path):
        if path == '/':
            self.current_directory = self.root
        elif path.startswith('/'):
            directories = path.split('/')[1:]
            current_dir = self.root
            for directory in directories:
                if directory in current_dir:
                    current_dir = current_dir[directory]
                else:
                    print(f"cd: {path}: No such file or directory")
                    return
            self.current_directory = current_dir
        else:
            print("cd: Invalid path. Use absolute paths starting with '/'.")

    def ls(self, path='.'):
        if path == '.':
            contents = self.current_directory.keys()
        elif path.startswith('/'):
            directories = path.split('/')[1:]
            current_dir = self.root
            for directory in directories:
                if directory in current_dir:
                    current_dir = current_dir[directory]
                else:
                    print(f"ls: {path}: No such file or directory")
                    return
            contents = current_dir.keys()
        else:
            print("ls: Invalid path. Use absolute paths starting with '/'.")

        print('\t'.join(contents))

    def grep(self, pattern, filename):
        if filename in self.current_directory:
            file_content = self.current_directory[filename]
            if isinstance(file_content, str) and pattern in file_content:
                print(file_content)
            else:
                print(f"grep: Pattern '{pattern}' not found in file '{filename}'.")
        else:
            print(f"grep: {filename}: No such file or directory.")

    def cat(self, filename):
        if filename in self.current_directory:
            file_content = self.current_directory[filename]
            if isinstance(file_content, str):
                print(file_content)
            else:
                print(f"cat: {filename}: Is a directory.")
        else:
            print(f"cat: {filename}: No such file or directory.")

    def touch(self, filename):
        if filename not in self.current_directory:
            self.current_directory[filename] = ''

    def echo(self, text, filename):
        if filename in self.current_directory:
            self.current_directory[filename] = text
        else:
            print(f"echo: {filename}: No such file or directory.")

    def mv(self, source, destination):
        if source in self.current_directory:
            source_content = self.current_directory[source]
            self.rm(source)
            if destination in self.current_directory:
                destination_content = self.current_directory[destination]
                if isinstance(destination_content, dict):
                    destination_content[source] = source_content
                else:
                    print(f"mv: {destination}: Not a directory.")
                    self.current_directory[source] = source_content
            else:
                self.current_directory[destination] = source_content
        else:
            print(f"mv: {source}: No such file or directory.")

    def cp(self, source, destination):
        if source in self.current_directory:
            source_content = self.current_directory[source]
            if destination in self.current_directory:
                destination_content = self.current_directory[destination]
                if isinstance(destination_content, dict):
                    destination_content[source] = source_content
                else:
                    print(f"cp: {destination}: Not a directory.")
            else:
                self.current_directory[destination] = source_content
        else:
            print(f"cp: {source}: No such file or directory.")

    def rm(self, path):
        if path in self.current_directory:
            if isinstance(self.current_directory[path], dict):
                del self.current_directory[path]
            else:
                print(f"rm: {path}: Is a directory. Use 'rm -r' to remove directories.")
        else:
            print(f"rm: {path}: No such file or directory.")

def main():
    file_system = InMemoryFileSystem()

    while True:
        command = input(f"{os.path.abspath('/')}$ ")

        # Split the command into operation and arguments
        parts = command.split()
        operation = parts[0]

        if operation == 'mkdir':
            if len(parts) >= 2:
                file_system.mkdir(parts[1])
            else:
                print("mkdir: Missing operand. Use 'mkdir <directory_name>'.")
        elif operation == 'cd':
            if len(parts) >= 2:
                file_system.cd(parts[1])
            else:
                print("cd: Missing operand. Use 'cd <directory_path>'.")
        elif operation == 'ls':
            path = parts[1] if len(parts) >= 2 else '.'
            file_system.ls(path)
        elif operation == 'grep':
            if len(parts) >= 3:
                file_system.grep(parts[1], parts[2])
            else:
                print("grep: Missing operand. Use 'grep <pattern> <filename>'.")
        elif operation == 'cat':
            if len(parts) >= 2:
                file_system.cat(parts[1])
            else:
                print("cat: Missing operand. Use 'cat <filename>'.")
        elif operation == 'touch':
            if len(parts) >= 2:
                file_system.touch(parts[1])
            else:
                print("touch: Missing operand. Use 'touch <filename>'.")
        elif operation == 'echo':
            if len(parts) >= 4 and parts[2] == '>':
                text = ' '.join(parts[1:2] + parts[3:])
                file_system.echo(text, parts[3])
            else:
                print("echo: Invalid syntax. Use 'echo <text> > <filename>'.")
        elif operation == 'mv':
            if len(parts) >= 3:
                file_system.mv(parts[1], parts[2])
            else:
                print("mv: Missing operand. Use 'mv <source> <destination>'.")
        elif operation == 'cp':
            if len(parts) >= 3:
                file_system.cp(parts[1], parts[2])
            else:
                print("cp: Missing operand. Use 'cp <source> <destination>'.")
        elif operation == 'rm':
            if len(parts) >= 2:
                file_system.rm(parts[1])
            else:
                print("rm: Missing operand. Use 'rm <path>'.")
        elif operation == 'exit':
            print("Exiting the file system. Goodbye!")
            break
        else:
            print(f"{operation}: Command not recognized.")

if __name__ == "__main__":
    main()
