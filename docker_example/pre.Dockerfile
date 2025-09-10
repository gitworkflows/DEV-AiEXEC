FROM khulnasoft/aiexec:1.0-alpha

CMD ["python", "-m", "aiexec", "run", "--host", "0.0.0.0", "--port", "7860"]
