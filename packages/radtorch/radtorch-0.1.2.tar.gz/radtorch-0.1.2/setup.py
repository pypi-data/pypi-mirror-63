from setuptools import setup

setup(
      name='radtorch',
      version='0.1.2',
      description='RADTorch, The Radiology Machine Learning Tool Kit',
      url='https://radtorch.github.io/radtorch/',
      author='Mohamed Elbanan, MD',
      license='MIT',
      packages=['radtorch'],
      install_requires=['torch', 'torchvision', 'numpy', 'pandas', 'pydicom', 'matplotlib', 'pillow', 'tqdm', 'sklearn', 'efficientnet-pytorch','pathlib'],
      zip_safe=False,
      classifiers=[
      "Development Status :: 4 - Beta",
      "License :: OSI Approved :: MIT License",
      "Natural Language :: English",
      "Programming Language :: Python :: 3 :: Only",
      "Topic :: Software Development :: Libraries :: Python Modules",
      ]
      )
