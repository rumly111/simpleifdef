# Sublime Text 3 plugin for highlighting #ifdef-#else-#endif
# in source code.
# Author: Joseph Botosh <rumly111@gmail.com>
# Licence: GPL

import sublime
import sublime_plugin


class IfdefHighlighter(sublime_plugin.EventListener):
	'''
	Scans whole text and searches for matching
	#ifdef-#else-#endif. Remembers their position.
	Then, when the cursor enters line with #ifdef/#else/#endif,
	all corresponding lines are highlighted
	'''

	def __init__(self, *args, **kw):
		super().__init__(*args,**kw)
		self._groups = dict()
		self._regions = []

	def _rescan(self, view):
		stack = []
		self._groups.clear()
		self._regions = view.find_by_selector("meta.preprocessor keyword.control.import")

		for r in self._regions:
			s = view.substr(r)

			if s.startswith('#if'):
				stack.append({(r.a, r.b)})  # Region is not hashable
			elif s in ('#elif', '#else'):
				if len(stack) > 0:
					stack[-1].add((r.a, r.b))
			elif s == '#endif':
				if len(stack) > 0:
					pset = stack.pop()
					pset.add((r.a, r.b))
					rlist = []
					for a, b in pset:
						rlist.append(sublime.Region(a, b))
					for p in pset:
						self._groups[p] = rlist

	def on_modified(self, view):
		self._rescan(view)

	def on_activated(self, view):
		self._rescan(view)

	def on_selection_modified(self, view):
		# NOTE: do I need to erase on each update?
		view.erase_regions('ifdef')
		cursor = view.sel()[0].a

		for r in self._regions:
			if r.contains(cursor):
				rtup = r.a, r.b
				if rtup in self._groups:
					view.add_regions('ifdef',self._groups[rtup],
						'keyword','',sublime.HIDE_ON_MINIMAP)
					break
