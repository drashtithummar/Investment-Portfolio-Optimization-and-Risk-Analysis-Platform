# This script optimizes portfolio using PyPortfolioOpt for parallel data sources
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.expected_returns import mean_historical_return
from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder.appName("PortfolioOptimization").getOrCreate()

# Load Data from S3
s3_path = "s3a://secure-portfolio-data/processed_data/"
data = spark.read.parquet(s3_path).toPandas()

def optimize_portfolio(data):
    pivot_data = data.pivot_table(values='daily_return', index='date', columns='symbol')
    mu = mean_historical_return(pivot_data)
    S = CovarianceShrinkage(pivot_data).ledoit_wolf()
    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    ef.portfolio_performance(verbose=True)
    return cleaned_weights

optimized_weights = optimize_portfolio(data)
print("Optimized Portfolio Weights:", optimized_weights)
