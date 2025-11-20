from setuptools import setup, find_packages

setup(
    name='finance_tracker',
    version='0.1.0',
    description='AI-powered personal finance tracker',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'streamlit',
        'supabase',
        'python-dotenv',
        'pandas',
        'numpy',
        'scikit-learn',
        'prophet',
        'plotly',
        'matplotlib',
        'seaborn'
    ]
)
