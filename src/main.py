from api.slave_controller import main
import sys

room = "office"

if len(sys.argv) == 2:
    room = sys.argv[1]

main(room)
