import requests
import time

BASE_URL = "https://api.mconnect.motorline.pt"

CONFIG_AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NWY1NDI2NmJiOGUzZThmZmQ3ZjJkNWYiLCJlbWFpbCI6ImNhdGFsaW4uZ2hlbmVhQGdtYWlsLmNvbSIsInR5cGUiOiJtY29ubmVjdF9mcmVlIiwiaG9tZV9pZCI6IjY1ZjU0Mjg1ZGIxYTliYzA2YjM3OGRkMSIsIm93bmVyIjp0cnVlLCJ3cml0ZSI6dHJ1ZSwiZGV2aWNlX2lkIjoiNjhkMmM2NTRlYTJjOGY2NWYwMTE4YjAwIiwiaWF0IjoxNzU5MDc5MTU3LCJleHAiOjE3NTkwODI3NTd9.GamNB_ki6mJJ0qMKQURCZHsslEvtLBqy3Xs_0ZXM7_w"
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

class Gate:
  state_map = ["Closed", "Unknown", "Open"]
  state_map_number = {
    "Closed": 0,
    "Open": 2
  }

  def __init__(self, user):
    self.id = "abc"
    self.name = "Generic Gate"
    self.roomName = "Generic Room"
    self.state = 0
    self.position = 0
    self.user = user

  def __str__(self):
    return f"[{self.roomName}] {self.name} state: {Gate.state_map[self.state]}; id: {self.id}"

  def getState(self):
    return Gate.state_map[self.state]

  def sendGateState(self, state):
    url = f"{BASE_URL}/devices/value/{self.id}"
    payload = {
      "value_id": "gate_state",
      "value": state
    }

    response = self.user.sendGateCmd(url, payload)
    return response.ok

  def close(self):
    if (self.state == 0):
      return

    if (self.sendGateState(0)):
      self.state = 2;
      self.position = 100

  def open(self):
    if (self.state == 2):
      return

    if (self.sendGateState(2)):
      self.state = 0;
      self.position = 100

  def setState(self, state):
    safeState = 0
    if (state >=0 and state <= 2):
      safeState = state
    self.state = safeState

  def setPosition(self, position):
    safePosition = 0
    if (position >=0 and position <= 100):
      safePosition = position

    self.position = safePosition


class AuthenticatedUser:
  def __init__(self):
    self.authToken = CONFIG_AUTH_TOKEN
    self.refreshToken = CONFIG_REFRESH_TOKEN
    self.baseHeaders =  {'Authorization': f'jwt {self.authToken}'}

  def get_rooms(self):
    response = requests.get(f'{BASE_URL}/{CONFIG_ROOMS_PATH}', headers=self.baseHeaders)
    if (not response.ok):
      return []
    return response.json()

  def get_homes(self):
    response = requests.get(f'{BASE_URL}/{CONFIG_HOMES_PATH}', headers=self.baseHeaders)
    print(response.json())

  def get_home(self):
    response = requests.get(f'{BASE_URL}/{CONFIG_HOME_PATH}', headers=self.baseHeaders)
    print(response.json())

  def sendGateCmd(self, URL, payload):
    response = requests.post(URL, headers=self.baseHeaders, json=payload)
    return response

  def refreshToken(self):
    pass

  def login(self, username, password):
    pass

  def selectHome(self, homeId):
    pass


def updateState(user, gates):
  roomsData = user.get_rooms()

  for room in roomsData:

    if "devices" not in room:
      continue

    for device in room["devices"]:

      id = device["_id"]

      gate = gates.get(id)
      if (gate is None):
        gate = Gate(user=user)
        gate.id = id
        gates[id] = gate

        gate.roomName = room["name"]
        gate.name = device["name"]

      for state in device["values"]:
        if (state["value_id"] == "gate_state"):
          gate.setState(state["value"])

        if (state["value_id"] == "gate_position"):
          gate.setPosition(state["value"])


if __name__ == "__main__":
  user = AuthenticatedUser()
  print(user.authToken)
  roomsData = user.get_rooms()

  # Parse room data
  gates = {}

  updateState(user, gates)

  for gateId in gates:
    print(gates[gateId])
    # gates[gateId].close()

  print("Sleeping for 5")
  time.sleep(5)

  updateState(user, gates)

  for gateId in gates:
    print(gates[gateId])
