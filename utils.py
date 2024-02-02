import requests

def get_data():
  #Set API's URL 
  api_url = "http://localhost:8000/get_wine_data"

  data_dict = {}
  try:
    # Try to connect and get response
    response = requests.get(api_url)
    # Check that there is no error code in the response
    if response.status_code != 200:
      print(f"Error: {response.status_code} - {response.text}")

    data_dict = response.json()['wine_data']
  except Exception as e:
    # If there is no response
    print(f"Error: {e}")
  
  # Return data as json
  return data_dict