s1 = __import__('sample.content.subpage1', fromlist=('*'))
s2 = __import__('sample.content.subpage2', fromlist=('*'))
s3 = __import__('sample.content.subpage3', fromlist=('*'))
# 'link' other pages
title = 'Home'
pages = [
			('subpage1', { var: getattr(s1, var) for var in dir(s1) if not var.startswith('_') }),
			('subpage2', { var: getattr(s2, var) for var in dir(s2) if not var.startswith('_') }),
			('subpage3', { var: getattr(s3, var) for var in dir(s3) if not var.startswith('_') })
		]

body = '<p>Lorem ipsum dolor sit amet</p>'
