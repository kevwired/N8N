const driveHelpers = require('../utils/drive-helpers');
const notionHelpers = require('../utils/notion-helpers');
const path = require('path');
const fs = require('fs').promises;

class FileManagementWorkflow {
  constructor() {
    this.supportedFormats = {
      documents: ['.txt', '.md', '.docx', '.pdf'],
      spreadsheets: ['.csv', '.xlsx', '.xls'],
      presentations: ['.pptx', '.ppt'],
      images: ['.jpg', '.jpeg', '.png', '.gif', '.svg'],
      archives: ['.zip', '.rar', '.7z']
    };
  }

  async organizeFiles(sourceFolder, targetStructure) {
    try {
      const files = await this.scanFolder(sourceFolder);
      const organizedStructure = await this.categorizeFiles(files);
      
      for (const [category, fileList] of Object.entries(organizedStructure)) {
        if (fileList.length > 0) {
          await this.createCategoryFolder(targetStructure[category] || category);
          await this.moveFiles(fileList, targetStructure[category] || category);
        }
      }

      return {
        processed_files: files.length,
        categories: Object.keys(organizedStructure),
        organization_complete: true,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('File organization failed:', error);
      throw error;
    }
  }

  async scanFolder(folderPath) {
    try {
      const entries = await fs.readdir(folderPath, { withFileTypes: true });
      const files = [];

      for (const entry of entries) {
        if (entry.isFile()) {
          files.push({
            name: entry.name,
            path: path.join(folderPath, entry.name),
            extension: path.extname(entry.name).toLowerCase(),
            stats: await fs.stat(path.join(folderPath, entry.name))
          });
        }
      }

      return files;
    } catch (error) {
      console.error('Folder scan failed:', error);
      return [];
    }
  }

  categorizeFiles(files) {
    const categories = {
      documents: [],
      spreadsheets: [],
      presentations: [],
      images: [],
      archives: [],
      others: []
    };

    files.forEach(file => {
      let categorized = false;
      
      for (const [category, extensions] of Object.entries(this.supportedFormats)) {
        if (extensions.includes(file.extension)) {
          categories[category].push(file);
          categorized = true;
          break;
        }
      }

      if (!categorized) {
        categories.others.push(file);
      }
    });

    return categories;
  }

  async createCategoryFolder(categoryPath) {
    try {
      await fs.mkdir(categoryPath, { recursive: true });
      return true;
    } catch (error) {
      console.error(`Failed to create folder ${categoryPath}:`, error);
      return false;
    }
  }

  async moveFiles(files, targetFolder) {
    const results = [];
    
    for (const file of files) {
      try {
        const targetPath = path.join(targetFolder, file.name);
        await fs.rename(file.path, targetPath);
        results.push({ file: file.name, status: 'moved', target: targetPath });
      } catch (error) {
        console.error(`Failed to move ${file.name}:`, error);
        results.push({ file: file.name, status: 'failed', error: error.message });
      }
    }

    return results;
  }

  async syncToGoogleDrive(localFolder, driveFolder) {
    try {
      const localFiles = await this.scanFolder(localFolder);
      const syncResults = [];

      for (const file of localFiles) {
        try {
          const driveFile = await driveHelpers.uploadFile(
            file.path,
            file.name,
            driveFolder
          );
          
          syncResults.push({
            local_file: file.name,
            drive_file_id: driveFile.id,
            status: 'synced'
          });
        } catch (error) {
          syncResults.push({
            local_file: file.name,
            status: 'failed',
            error: error.message
          });
        }
      }

      return {
        synced_files: syncResults.filter(r => r.status === 'synced').length,
        failed_files: syncResults.filter(r => r.status === 'failed').length,
        results: syncResults,
        sync_timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Google Drive sync failed:', error);
      throw error;
    }
  }

  async createFileIndex(folderPath, indexName = 'file-index') {
    try {
      const files = await this.scanFolder(folderPath);
      const index = {
        created_at: new Date().toISOString(),
        folder_path: folderPath,
        total_files: files.length,
        files: files.map(file => ({
          name: file.name,
          extension: file.extension,
          size: file.stats.size,
          modified: file.stats.mtime,
          created: file.stats.birthtime
        }))
      };

      const indexPath = path.join(folderPath, `${indexName}.json`);
      await fs.writeFile(indexPath, JSON.stringify(index, null, 2));

      return {
        index_file: indexPath,
        indexed_files: files.length,
        index_created: true
      };
    } catch (error) {
      console.error('File indexing failed:', error);
      throw error;
    }
  }

  async logToNotion(operation, results, databaseId) {
    return await notionHelpers.createPage(databaseId, {
      title: `File Operation: ${operation}`,
      operation_type: operation,
      results: JSON.stringify(results),
      status: 'Completed',
      timestamp: new Date().toISOString()
    });
  }
}

module.exports = FileManagementWorkflow;