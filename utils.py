import requests

def get_data():
  api_url = "http://localhost:8000/get_wine_data"
  data_dict = {}
  try:
    response = requests.get(api_url)
    if response.status_code != 200:
      print(f"Error: {response.status_code} - {response.text}")
    data_dict = response.json()['wine_data']
  except Exception as e:
    print(f"Error: {e}")
  return data_dict