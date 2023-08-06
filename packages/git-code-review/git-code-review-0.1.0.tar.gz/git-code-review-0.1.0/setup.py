from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as long_d_f:
    long_description = long_d_f.read()

setup(
  name='git-code-review',
  version='0.1.0',
  py_modules=['git_code_review'],
  description='Git Code Review',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='Jeff Caffrey-Hill',
  author_email='jeff@reverentengineer.com',
  url='https://github.com/ReverentEngineer/git-code-review',
  keywords=['git', 'code', 'review', 'cli'],
  classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Apache Software License',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 3',
      ],
  entry_points={
      'console_scripts': [
            'git-code-review=git_code_review:main'
        ]
    },
  extras_require={
    'dev': ['pyflake8']
    }
)
