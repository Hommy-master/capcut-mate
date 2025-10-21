import subprocess
import json
import time

def get_video_duration(video_url):
    """
    Get video duration with timeout retry support.
    :param video_url: Video URL
    :return: Video duration (seconds)
    """
    
    # Define retry count and wait time for each retry
    max_retries = 3
    retry_delay_seconds = 1 # 1 second interval between retries
    timeout_seconds = 10 # Set timeout for each attempt

    for attempt in range(max_retries):
        print(f"Attempting to get video duration (Attempt {attempt + 1}/{max_retries}) ...")
        result = {"success": False, "output": 0, "error": None} # Reset result before each retry
        
        try:
            command = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'stream=duration',
                '-show_entries', 'format=duration',
                '-print_format', 'json',
                video_url
            ]
            
            # Use subprocess.run for more flexible handling of timeout and output
            process = subprocess.run(command, 
                                     capture_output=True, 
                                     text=True, # Auto decode to text
                                     timeout=timeout_seconds, # Use variable to set timeout
                                     check=True) # Raise CalledProcessError if non-zero exit code

            info = json.loads(process.stdout)
            
            # Prioritize getting duration from streams because it's more accurate
            media_streams = [s for s in info.get('streams', []) if 'duration' in s]
            
            if media_streams:
                duration = float(media_streams[0]['duration'])
                result["output"] = duration
                result["success"] = True
            # Otherwise get duration from format information
            elif 'format' in info and 'duration' in info['format']:
                duration = float(info['format']['duration'])
                result["output"] = duration
                result["success"] = True
            else:
                result["error"] = "Audio/video duration information not found."
            
            # If duration is successfully obtained, return result directly without retrying
            if result["success"]:
                print(f"Successfully obtained duration: {result['output']:.2f} seconds")
                return result

        except subprocess.TimeoutExpired:
            result["error"] = f"Getting video duration timed out (exceeded {timeout_seconds} seconds)."
            print(f"Attempt {attempt + 1} timed out.")
        except subprocess.CalledProcessError as e:
            result["error"] = f"Error executing ffprobe command (exit code {e.returncode}): {e.stderr.strip()}"
            print(f"Attempt {attempt + 1} failed. Error: {e.stderr.strip()}")
        except json.JSONDecodeError as e:
            result["error"] = f"Error parsing JSON data: {e}"
            print(f"Attempt {attempt + 1} failed. JSON parsing error: {e}")
        except FileNotFoundError:
            result["error"] = "ffprobe command not found. Please ensure FFmpeg is installed and in system PATH."
            print("Error: ffprobe command not found, please check installation.")
            return result # No need to retry if ffprobe itself is not found
        except Exception as e:
            result["error"] = f"Unknown error occurred: {e}"
            print(f"Attempt {attempt + 1} failed. Unknown error: {e}")
        
        # Try using remote service to get duration after each local failure
        if not result["success"]:
            print(f"Local retrieval failed")
            # try:
            #     remote_duration = get_duration(video_url)
            #     if remote_duration is not None:
            #         result["success"] = True
            #         result["output"] = remote_duration
            #         result["error"] = None
            #         print(f"Remote service successfully obtained duration: {remote_duration:.2f} seconds")
            #         return result  # Remote service succeeded, return directly
            #     else:
            #         print(f"Remote service also unable to get duration (Attempt {attempt + 1})")
            # except Exception as e:
            #     print(f"Remote service failed to get duration (Attempt {attempt + 1}): {e}")
        
        # If current attempt failed and max retries not reached, wait and prepare for next retry
        if not result["success"] and attempt < max_retries - 1:
            print(f"Waiting {retry_delay_seconds} seconds before retrying...")
            time.sleep(retry_delay_seconds)
        elif not result["success"] and attempt == max_retries - 1:
            print(f"Maximum retry count {max_retries} reached, both local and remote services unable to get duration.")
            
    return result # Return the last failure result after all retries fail