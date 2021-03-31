#!/bin/bash
aws s3 cp data/outputs/folia_output/folia.zip s3://fortunoff-secrets/let-them-speak-staging-data/folia.zip --profile lts-staging
aws s3 cp data/outputs/db/lts.archive s3://fortunoff-secrets/let-them-speak-staging-data/lts.archive --profile lts-staging