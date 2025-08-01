const driveConfig = require('../api-configs/google-drive-config');
const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

class DriveHelpers {
  constructor() {
    this.config = driveConfig;
    this.drive = null;
    this.authenticated = false;
  }

  async authenticate() {
    try {
      const auth = new google.auth.GoogleAuth({
        keyFile: this.config.serviceAccountKeyFile,
        scopes: this.config.scopes,
      });

      const authClient = await auth.getClient();
      this.drive = google.drive({ version: 'v3', auth: authClient });
      this.authenticated = true;
      
      return true;
    } catch (error) {
      console.error('Google Drive authentication failed:', error);
      throw error;
    }
  }

  async ensureAuthenticated() {
    if (!this.authenticated) {
      await this.authenticate();
    }
  }

  async uploadFile(filePath, fileName, folderId) {
    await this.ensureAuthenticated();
    
    try {
      const fileMetadata = {
        name: fileName || path.basename(filePath),
        parents: folderId ? [folderId] : undefined
      };

      const media = {
        body: fs.createReadStream(filePath)
      };

      const response = await this.drive.files.create({
        requestBody: fileMetadata,
        media: media,
        fields: 'id,name,size,createdTime'
      });

      return response.data;
    } catch (error) {
      console.error('File upload failed:', error);
      throw error;
    }
  }

  async uploadTextFile(content, fileName, folderId) {
    await this.ensureAuthenticated();
    
    try {
      const fileMetadata = {
        name: fileName,
        parents: folderId ? [folderId] : undefined
      };

      const media = {
        mimeType: 'text/plain',
        body: content
      };

      const response = await this.drive.files.create({
        requestBody: fileMetadata,
        media: media,
        fields: 'id,name,size,createdTime'
      });

      return response.data;
    } catch (error) {
      console.error('Text file upload failed:', error);
      throw error;
    }
  }

  async createFolder(folderName, parentFolderId) {
    await this.ensureAuthenticated();
    
    try {
      const fileMetadata = {
        name: folderName,
        mimeType: 'application/vnd.google-apps.folder',
        parents: parentFolderId ? [parentFolderId] : undefined
      };

      const response = await this.drive.files.create({
        requestBody: fileMetadata,
        fields: 'id,name'
      });

      return response.data;
    } catch (error) {
      console.error('Folder creation failed:', error);
      throw error;
    }
  }

  async listFiles(folderId, pageSize = 10) {
    await this.ensureAuthenticated();
    
    try {
      const query = folderId ? `'${folderId}' in parents` : undefined;
      
      const response = await this.drive.files.list({
        q: query,
        pageSize: pageSize,
        fields: 'files(id,name,mimeType,size,createdTime,modifiedTime)'
      });

      return response.data.files;
    } catch (error) {
      console.error('File listing failed:', error);
      throw error;
    }
  }

  async downloadFile(fileId, destinationPath) {
    await this.ensureAuthenticated();
    
    try {
      const response = await this.drive.files.get({
        fileId: fileId,
        alt: 'media'
      }, { responseType: 'stream' });

      const dest = fs.createWriteStream(destinationPath);
      response.data.pipe(dest);

      return new Promise((resolve, reject) => {
        dest.on('finish', () => resolve(destinationPath));
        dest.on('error', reject);
      });
    } catch (error) {
      console.error('File download failed:', error);
      throw error;
    }
  }

  async deleteFile(fileId) {
    await this.ensureAuthenticated();
    
    try {
      await this.drive.files.delete({
        fileId: fileId
      });
      
      return true;
    } catch (error) {
      console.error('File deletion failed:', error);
      throw error;
    }
  }

  async shareFile(fileId, emailAddress, role = 'reader') {
    await this.ensureAuthenticated();
    
    try {
      const permission = {
        type: 'user',
        role: role,
        emailAddress: emailAddress
      };

      const response = await this.drive.permissions.create({
        fileId: fileId,
        requestBody: permission,
        fields: 'id'
      });

      return response.data;
    } catch (error) {
      console.error('File sharing failed:', error);
      throw error;
    }
  }

  async getFileMetadata(fileId) {
    await this.ensureAuthenticated();
    
    try {
      const response = await this.drive.files.get({
        fileId: fileId,
        fields: 'id,name,mimeType,size,createdTime,modifiedTime,parents,webViewLink'
      });

      return response.data;
    } catch (error) {
      console.error('Failed to get file metadata:', error);
      throw error;
    }
  }

  async searchFiles(query, mimeType = null) {
    await this.ensureAuthenticated();
    
    try {
      let searchQuery = `name contains '${query}'`;
      if (mimeType) {
        searchQuery += ` and mimeType='${mimeType}'`;
      }

      const response = await this.drive.files.list({
        q: searchQuery,
        fields: 'files(id,name,mimeType,size,createdTime)'
      });

      return response.data.files;
    } catch (error) {
      console.error('File search failed:', error);
      throw error;
    }
  }

  async moveFile(fileId, newParentFolderId) {
    await this.ensureAuthenticated();
    
    try {
      // Get current parents
      const file = await this.drive.files.get({
        fileId: fileId,
        fields: 'parents'
      });

      const previousParents = file.data.parents.join(',');

      // Move file
      const response = await this.drive.files.update({
        fileId: fileId,
        addParents: newParentFolderId,
        removeParents: previousParents,
        fields: 'id,parents'
      });

      return response.data;
    } catch (error) {
      console.error('File move failed:', error);
      throw error;
    }
  }
}

module.exports = new DriveHelpers();