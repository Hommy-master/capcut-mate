
import oss2
import os
from settings.local import OSS_CONFIG, MP4_OSS_CONFIG

def upload_to_oss(path):
    # Create OSS client
    auth = oss2.Auth(OSS_CONFIG['access_key_id'], OSS_CONFIG['access_key_secret'])
    bucket = oss2.Bucket(auth, OSS_CONFIG['endpoint'], OSS_CONFIG['bucket_name'])
    
    # Upload file
    object_name = os.path.basename(path)
    bucket.put_object_from_file(object_name, path)
    
    # Generate signed URL (valid for 24 hours)
    url = bucket.sign_url('GET', object_name, 24 * 60 * 60)
    
    # Clean up temporary file
    os.remove(path)
    
    return url

def upload_mp4_to_oss(path):
    """Special method for uploading MP4 files, using custom domain and v4 signature"""
    # Directly use credentials from the configuration file
    auth = oss2.AuthV4(MP4_OSS_CONFIG['access_key_id'], MP4_OSS_CONFIG['access_key_secret'])
    
    # Create OSS client with custom domain
    bucket = oss2.Bucket(
        auth, 
        MP4_OSS_CONFIG['endpoint'], 
        MP4_OSS_CONFIG['bucket_name'], 
        region=MP4_OSS_CONFIG['region'], 
        is_cname=True
    )
    
    # Upload file
    object_name = os.path.basename(path)
    bucket.put_object_from_file(object_name, path)
    
    # Generate pre-signed URL (valid for 24 hours), set slash_safe to True to avoid path escaping
    url = bucket.sign_url('GET', object_name, 24 * 60 * 60, slash_safe=True)
    
    # Clean up temporary file
    os.remove(path)
    
    return url