#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
English sentiment analysis module using NLTK's VADER.

This module analyzes sentiment in text using NLTK's VADER sentiment analyzer.
It can process individual strings or CSV files containing messages.
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Any, Dict, List, Optional

import pandas as pd  # type: ignore
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # type: ignore

# Constants
DEFAULT_OUTPUT_DIR: str = "output"
DEFAULT_OUTPUT_FILE: str = os.path.join(DEFAULT_OUTPUT_DIR, "salida-con-sentimiento.csv")
DEFAULT_MESSAGE_COLUMN: str = "mensaje"
DEFAULT_SENTIMENT_COLUMN: str = "sentimiento"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Class for analyzing sentiment in text using VADER."""

    def __init__(self) -> None:
        """Initialize the sentiment analyzer with VADER."""
        try:
            self.analyzer = SentimentIntensityAnalyzer()
            logger.debug("SentimentIntensityAnalyzer initialized successfully")
        except Exception as exc:
            logger.error("Failed to initialize SentimentIntensityAnalyzer: %s", exc)
            raise

    def get_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a single text string.

        Args:
            text: The text to analyze

        Returns:
            Dictionary with sentiment scores (neg, neu, pos, compound)

        Raises:
            ValueError: If text is None
        """
        if text is None:
            logger.error("None value provided for text analysis")
            raise ValueError("Text cannot be None")

        if not isinstance(text, str):
            logger.warning("Non-string input provided, converting to string: %r", text)
            text = str(text)

        if not text.strip():
            logger.warning("Empty text provided for analysis")

        return self.analyzer.polarity_scores(text)

    def analyze_file(
        self,
        filepath: str,
        message_column: str = DEFAULT_MESSAGE_COLUMN,
        sentiment_column: str = DEFAULT_SENTIMENT_COLUMN,
    ) -> pd.DataFrame:
        """
        Analyze sentiment in a CSV file with messages.

        Args:
            filepath: Path to the CSV file
            message_column: Name of the column containing messages
            sentiment_column: Name of the column to store sentiment scores

        Returns:
            DataFrame with original data plus sentiment scores

        Raises:
            FileNotFoundError: If the input file doesn't exist
            KeyError: If the message column doesn't exist in the CSV
            ValueError: If the file is empty or filepath is invalid
        """
        # Validate inputs
        if not filepath:
            logger.error("Empty filepath provided")
            raise ValueError("Filepath cannot be empty")

        # Ensure input file exists
        if not os.path.exists(filepath):
            logger.error("Input file not found: %s", filepath)
            raise FileNotFoundError(f"Input file not found: {filepath}")

        # Read data
        try:
            dframe = pd.read_csv(filepath)
            logger.info("Successfully loaded %d rows from %s", len(dframe), filepath)
        except pd.errors.EmptyDataError:
            logger.error("The file %s is empty", filepath)
            raise ValueError(f"The file {filepath} is empty")
        except Exception as exc:
            logger.error("Error reading CSV file: %s", exc)
            raise

        # Verify column exists
        if message_column not in dframe.columns:
            logger.error("Column '%s' not found in %s", message_column, filepath)
            raise KeyError(f"Column '{message_column}' not found in {filepath}")

        # Apply sentiment analysis
        logger.info("Analyzing sentiment for column '%s'", message_column)

        # Create a safe apply function
        def safe_sentiment(value: Any) -> float:
            """Safely get compound sentiment score."""
            try:
                return self.get_sentiment(str(value))["compound"]
            except Exception as exc:
                logger.warning("Error analyzing text: %s. Text: %r", exc, value)
                return 0.0

        dframe[sentiment_column] = dframe[message_column].apply(safe_sentiment)

        return dframe

    @staticmethod
    def save_results(
        dframe: pd.DataFrame,
        output_path: str = DEFAULT_OUTPUT_FILE,
    ) -> str:
        """
        Save analysis results to CSV file.

        Args:
            dframe: DataFrame with sentiment analysis results
            output_path: Path where to save the results

        Returns:
            Path to the saved file

        Raises:
            ValueError: If DataFrame is empty or output_path is invalid
        """
        if dframe.empty:
            logger.error("Cannot save empty DataFrame")
            raise ValueError("DataFrame is empty")

        if not output_path:
            logger.error("Empty output path provided")
            raise ValueError("Output path cannot be empty")

        # Create output directory
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            logger.debug("Created output directory: %s", output_dir)

        # Export results
        try:
            dframe.to_csv(output_path, index=False)
            logger.info("Results saved to %s", output_path)
            return output_path
        except Exception as exc:
            logger.error("Error saving results: %s", exc)
            raise


def get_sentiment_label(compound_score: float) -> str:
    """
    Get a human-readable sentiment label based on compound score.

    Args:
        compound_score: The compound sentiment score (-1 to 1)

    Returns:
        String label: "positive", "negative", or "neutral"
    """
    if compound_score >= 0.05:
        return "positive"
    if compound_score <= -0.05:
        return "negative"
    return "neutral"


def analyze_examples() -> None:
    """Analyze example sentences and print results."""
    examples: List[str] = [
        "It is a charming and beautiful product",
        "It was a horrible experience",
        "I have nothing to say. Normal so far.",
    ]

    analyzer = SentimentAnalyzer()

    for example in examples:
        sentiment = analyzer.get_sentiment(example)
        compound = sentiment["compound"]
        sentiment_label = get_sentiment_label(compound)

        print(f"Text: '{example}'")
        print(f"Sentiment: {sentiment}")
        print(f"Label: {sentiment_label}")
        print()


def main() -> int:
    """
    Run the main program.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Analyze example sentences
        analyze_examples()

        # Analyze file
        analyzer = SentimentAnalyzer()
        input_file = "data/reviews.csv"

        logger.info("Starting analysis of file: %s", input_file)
        result = analyzer.analyze_file(input_file)

        output_file = analyzer.save_results(result)
        print(f"\nResults saved to {output_file}")

        print("\nFirst 5 rows:")
        print(result.head())

        return 0
    except FileNotFoundError as exc:
        logger.error("File not found: %s", exc)
        print(f"Error: {exc}")
        return 1
    except KeyError as exc:
        logger.error("Column not found: %s", exc)
        print(f"Error: {exc}")
        return 1
    except Exception as exc:
        logger.error("Unexpected error: %s", exc, exc_info=True)
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())






