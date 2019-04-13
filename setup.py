from distutils.core import setup

setup(name='mafgraph',
      version='0.1',
      description='MAF sorter',
      author='Anna Lisiecka',
      url='https://github.com/anialisiecka/Mafgraph',
      packages=['mafgraph', 'mafgraph.graph'],
      install_requires=['biopython', 'networkx']
     )