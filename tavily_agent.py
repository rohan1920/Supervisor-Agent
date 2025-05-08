
from datetime import datetime
import pytz

def get_islamabad_time():
    pakistan_tz = pytz.timezone("Asia/Karachi")  # Islamabad time is same as Karachi
    time_in_pk = datetime.now(pakistan_tz)
    return time_in_pk.strftime("%Y-%m-%d %I:%M %p")

# Example usage
if __name__ == "__main__":
    print("Current time in Islamabad:", get_islamabad_time())
