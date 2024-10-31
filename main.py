from config import *
import analizer, csv_converter


def main():
    print()
    print()
    print(f"<{' Analizing Chess Games ':=^88}>")

    # Analize and summarize data and save as dictionary and text
    analizer.run()

    # Turn into csv files
    csv_converter.run()
    return


if __name__ == "__main__":
    main()
