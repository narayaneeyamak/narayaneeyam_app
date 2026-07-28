/**
 * Converts Google Drive sharing links to direct audio stream URLs.
 */
export function getAudioStreamUrl(url) {
  if (!url) return '';
  
  // Direct audio URLs (mp3, m4a, wav, etc.)
  if (!url.includes('drive.google.com')) {
    return url;
  }

  // Extract file ID from /file/d/FILE_ID/ or ?id=FILE_ID
  let fileId = '';
  const fileDMatch = url.match(/\/file\/d\/([a-zA-Z0-9_-]+)/);
  if (fileDMatch && fileDMatch[1]) {
    fileId = fileDMatch[1];
  } else {
    const idParamMatch = url.match(/[?&]id=([a-zA-Z0-9_-]+)/);
    if (idParamMatch && idParamMatch[1]) {
      fileId = idParamMatch[1];
    }
  }

  if (fileId) {
    // Return direct download/stream link format
    return `https://drive.usercontent.google.com/download?id=${fileId}&export=download`;
  }

  return url;
}

export function getGoogleDriveViewUrl(url) {
  if (!url) return '#';
  return url;
}
