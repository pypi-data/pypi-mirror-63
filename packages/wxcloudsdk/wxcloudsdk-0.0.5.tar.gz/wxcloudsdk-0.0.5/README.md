This package is maintained by Typing Cat<liuchunyao0321@gmail.com>.

This package is useful for developing wechat miniprogram. Especially for the cloud apis.

## API usage

### upload_file: (token, env_id, cloud_path, cloud_dir, local_path)
Upload a single file to wx cloud storage

### rebuild: (file_path, env_id, token, collection_name)
Refresh a collection by remove and rebuild a collection. NOTICE that you must upload the data file to the cloud storage first. File path is the cloud file path, not local path.
