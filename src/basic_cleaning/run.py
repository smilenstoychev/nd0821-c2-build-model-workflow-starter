#!/usr/bin/env python
"""
Longer description of the same
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    
    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    local_path = wandb.use_artifact("sample.csv:latest").file()
    logger.info("Reading dataframe from csv...")
    df = pd.read_csv(local_path)    
    logger.info("Done reading dataframe.")

    # import pandas_profiling

    # logger.info("Starting to profile data...")
    # profile = pandas_profiling.ProfileReport(df)
    # profile.to_widgets()
    # logger.info("Done profiling data.")

    # Drop outliers
    logger.info("Dropping outliers...")
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    logger.info("Done dropping outliers.")
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    logger.info("Done converting to datetime.")

    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    df.to_csv("clean_sample.csv", index=False)
    logger.info("Done saving to disk.")

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description)
    artifact.add_file("clean_sample.csv")
    logger.info("Uploading to wandb...")
    run.log_artifact(artifact)
    logger.info("Done uploading to wandb.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Basic data cleaning.")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="The name of the input artifact to be used",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="The name to be used for the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="The type of output file",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="The description to be attached to output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="The min valid price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="The max valid price",
        required=True
    )


    args = parser.parse_args()

    go(args)
