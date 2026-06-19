import logging
import csv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def sort_words_by_frequency(list_file, freq_csv, output_file):
    # 1. Process the CSV frequency file and build dictionary {word: count}
    word_counts = {}
    logging.info(f"Attempting to read the frequency CSV file: {freq_csv}")
    try:
        with open(freq_csv, mode="r", encoding="utf-8") as f:
            # Use DictReader to automatically map headers (word, count)
            reader = csv.DictReader(f)
            for row_num, row in enumerate(
                reader, start=2
            ):  # start=2 because row 1 is header
                try:
                    word = row["word"].strip().lower()
                    count = int(row["count"])
                    if word and word not in word_counts:
                        word_counts[word] = count
                except (KeyError, ValueError) as e:
                    logging.warning(
                        f"Skipping invalid data at row {row_num}: {row} - Error: {e}"
                    )

        logging.info(
            f"Successfully loaded {len(word_counts)} words from the frequency CSV."
        )
    except FileNotFoundError:
        logging.error(
            f"File not found: {freq_csv}. Please ensure it exists in the current directory."
        )
        return

    # 2. Process the list of words to be sorted
    logging.info(f"Attempting to read the target word list: {list_file}")
    try:
        with open(list_file, mode="r", encoding="utf-8") as f:
            # Strip whitespace and ignore empty lines
            words_to_sort = [line.strip() for line in f if line.strip()]
        logging.info(f"Successfully loaded {len(words_to_sort)} words to sort.")
    except FileNotFoundError:
        logging.error(
            f"File not found: {list_file}. Please ensure it exists in the current directory."
        )
        return

    # 3. Verification
    logging.info("Verifying word matches...")
    unmatched_words = [
        word for word in words_to_sort if word.lower() not in word_counts
    ]

    if unmatched_words:
        logging.warning(
            f"Verification found {len(unmatched_words)} word(s) not present in the CSV file."
        )
        sample_size = min(5, len(unmatched_words))
        logging.warning(
            f"Sample of unmatched words (will be treated as count=0): {', '.join(unmatched_words[:sample_size])}..."
        )
    else:
        logging.info("Perfect match! All words were found in the frequency CSV.")

    # 4. Sort
    # Get the count for each word. If not found, default to 0.
    # Set reverse=True to sort from highest frequency to lowest.
    logging.info("Sorting words based on frequency counts...")
    sorted_words = sorted(
        words_to_sort, key=lambda w: word_counts.get(w.lower(), 0), reverse=True
    )

    # 5. Write the sorted results to the output file
    logging.info(f"Writing sorted results to {output_file}...")
    try:
        with open(output_file, mode="w", encoding="utf-8") as f:
            for word in sorted_words:
                f.write(word + "\n")
        logging.info(
            f"Sorting completed! Processed {len(words_to_sort)} words. Results saved to '{output_file}'."
        )
    except Exception as e:
        logging.error(f"An error occurred while writing to the output file: {e}")


if __name__ == "__main__":
    INPUT_LIST = "American Oxford 5000.txt"
    FREQ_LIST = "english-word-frequency.csv"
    OUTPUT_LIST = "American Oxford 5000 Sorted.txt"

    sort_words_by_frequency(INPUT_LIST, FREQ_LIST, OUTPUT_LIST)
