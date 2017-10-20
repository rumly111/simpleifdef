# Sublime Text 3 plugin for highlighting #ifdef-#else-#endif
# in source code.
# Author: Joseph Botosh <rumly111@gmail.com>
# License: GPL

import sublime
import sublime_plugin


class IfdefHighlighter(sublime_plugin.EventListener):
	'''
	Scans whole text and searches for matching
	#ifdef-#else-#endif. Remembers their position.
	Then, when the cursor is on #ifdef/#else/#endif,
	all corresponding keywords are highlighted.
	Supports simple error checking
	'''

	def __init__(self, *args, **kw):
		super().__init__(*args,**kw)
		self._groups = dict()
		self._regions = []

	def _rescan(self, view):
		self._groups.clear()
		self._regions.clear()
		stack = []
		errors = []
		regions = view.find_by_selector("meta.preprocessor keyword.control.import")

		for r in regions:
			s = view.substr(r)

			if s.startswith('#if'):
				self._regions.append(r)
				stack.append({(r.a, r.b)})  # Region is not hashable
			elif s in ('#elif', '#else'):
				if len(stack) > 0:
					self._regions.append(r)
					stack[-1].add((r.a, r.b))
				else:
					errors.append(r)
			elif s == '#endif':
				if len(stack) > 0:
					self._regions.append(r)
					pset = stack.pop()
					pset.add((r.a, r.b))
					rlist = []
					for a, b in pset:
						rlist.append(sublime.Region(a, b))
					for p in pset:
						self._groups[p] = rlist
				else:
					errors.append(r)

		for p in stack:
			errors.extend(sublime.Region(t[0], t[1]) for t in p)

		view.erase_regions('ifdeferror')
		if errors:
			view.add_regions('ifdeferror', errors, 'invalid', '', 0)

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
