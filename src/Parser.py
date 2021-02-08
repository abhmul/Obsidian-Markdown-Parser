import os
from src.MarkdownFile import MarkdownFile

class Parser:
    def __init__(self, folderPath='.'):
        self._folderPath = folderPath
        self.mdFiles = list[MarkdownFile]
        self._retrieveMarkdownFiles()


    def _retrieveMarkdownFiles(self):
        """Directory traversal to find all .md files and stores them in _mdFiles

        Full credit goes to: https://github.com/archelpeg
        """
        self.mdFiles = []
        for dirpath, _, files in os.walk(self._folderPath):
            # print(f'Found directory: {dirpath}')
            for file_name in files:
                if file_name.endswith('.md'):
                    normalised_path = os.path.normpath(dirpath + "/" + file_name) # normalises path for current file system
                    file = MarkdownFile(file_name, normalised_path)
                    self.mdFiles.append(file)

    def searchFilesWithTag(self, tag=None):
        """Find all files containing a specific tag
        """
        files = set()
        if tag == None:
            return files
        for file in self.mdFiles:
            if tag in file.tags:
                files.add(file)
        return files

    def findSubFilesForFiles(self, files: set):
        """Iteration to grow files while i can"""
        while not self._grow(files):
            pass
        return files


    def _grow(self, files):
        """Add new files found following links in files and stores them in files"""
        addedFiles = set()
        for file in files:
            linkedFiles = file.links
            linkedFiles = [link for link in linkedFiles] # Added .md at the end
            linkedFiles = [file # Get the full links
                for file in self.mdFiles
                for link in linkedFiles
                if link in file.fileName
            ]
            linkedFiles = set(linkedFiles) - files # Only keep not added files
            print(linkedFiles)
            for link in linkedFiles:
                addedFiles.add(link)
        for file in addedFiles:
            files.add(file)
        return len(addedFiles) == 0