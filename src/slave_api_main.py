from api.slave_controller import main
import sys

# Launches the slave api with sensor/room name given as cmd arg.

room = "office"

if len(sys.argv) == 2:
    room = sys.argv[1]

main(room)
