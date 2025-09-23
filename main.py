import requests

BASE_URL = "https://api.mconnect.motorline.pt"

CONFIG_AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NWY1NDI2NmJiOGUzZThmZmQ3ZjJkNWYiLCJlbWFpbCI6ImNhdGFsaW4uZ2hlbmVhQGdtYWlsLmNvbSIsInR5cGUiOiJtY29ubmVjdF9mcmVlIiwiaG9tZV9pZCI6IjY1ZjU0Mjg1ZGIxYTliYzA2YjM3OGRkMSIsIm93bmVyIjp0cnVlLCJ3cml0ZSI6dHJ1ZSwiZGV2aWNlX2lkIjoiNjhkMmM2NTRlYTJjOGY2NWYwMTE4YjAwIiwiaWF0IjoxNzU4NjQ0MzAxLCJleHAiOjE3NTg2NDc5MDF9.zbwj1cGw0XQz79gsvX8giVnGJClWq1UwxK8L5sBoMVo"
CONFIG_REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NWY1NDI2NmJiOGUzZThmZmQ3ZjJkNWYiLCJlbWFpbCI6ImNhdGFsaW4uZ2hlbmVhQGdtYWlsLmNvbSIsInR5cGUiOiJtY29ubmVjdF9mcmVlIiwiZGV2aWNlX2lkIjoiNjhkMmM2NTRlYTJjOGY2NWYwMTE4YjAwIiwicmVmcmVzaF90b2tlbiI6dHJ1ZSwiaWF0IjoxNzU4NjQzNzk3LCJleHAiOjE3NzQxOTU3OTd9.MPuKCLVgtVENE4KwD2orLjC9LCQsrzTjZHmB3d_gDj0"

CONFIG_ROOMS_PATH = "rooms"
CONFIG_HOMES_PATH = "homes"
CONFIG_HOME_PATH = "home"
# HOMES and HOMES seem to retrieve the same thing. In our case at least
# One is a list of homes, the other I think is the currently selected home


# 1. Token
# 2. Verify for MFA
# 3. Homes
# 4. Home -> will return the home that the token is for
# 5. Rooms -> this will get all the devices and data that we need.

class AuthenticatedUser:
  def __init__(self):
    self.authToken = CONFIG_AUTH_TOKEN
    self.refreshToken = CONFIG_REFRESH_TOKEN
    self.baseHeaders =  {'Authorization': f'jwt {self.authToken}'}

  def get_rooms(self):
    response = requests.get(f'{BASE_URL}/{CONFIG_ROOMS_PATH}', headers=self.baseHeaders)
    print(response.json())

  def get_homes(self):
    response = requests.get(f'{BASE_URL}/{CONFIG_HOMES_PATH}', headers=self.baseHeaders)
    print(response.json())

  def get_home(self):
    response = requests.get(f'{BASE_URL}/{CONFIG_HOME_PATH}', headers=self.baseHeaders)
    print(response.json())


if __name__ == "__main__":
  user = AuthenticatedUser()
  print(user.authToken)
  user.get_rooms()
