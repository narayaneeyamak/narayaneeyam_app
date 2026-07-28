/**
 * Converts Google Drive sharing links to direct audio stream URLs.
 * Handles formats like:
 * - https://drive.google.com/file/d/FILE_ID/view?usp=drive_link
 * - https://drive.google.com/open?id=FILE_ID
 * - Direct audio URLs (mp3, wav, etc.)
 */
export function getAudioStreamUrl(url) {
  if (!url) return '';
  
  // If it's already a direct link or not Google Drive
  if (!url.includes('drive.google.com')) {
    return url;
  }

  // Extract file ID from file/d/ID/ or ?id=ID
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
    // Return Google Drive direct streaming export URL
    return `https://docs.google.com/uc?export=download&id=${fileId}`;
  }

  return url;
}
