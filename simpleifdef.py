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
		self._regions = dict()

	def _rescan(self, view):
		stack = []
		i = -1
		R = sublime.Region(0, view.size())
		self._groups.clear()
		self._regions.clear()

		for line in view.lines(R):
			i += 1
			la = line.a

			while view.substr(la) in (' ', '\t'):
				la += 1

			if view.substr(la) != '#':
				continue

			r = view.find('#[a-z]+', la)
			if not r:
				continue

			self._regions[i] = r
			s = view.substr(r)

			if s.startswith('#if'):
				stack.append({i})
			elif s in ('#elif', '#else'):
				if len(stack) > 0:
					stack[-1].add(i)
			elif s == '#endif':
				if len(stack) > 0:
					ll = stack.pop()
					ll.add(i)
					for l in ll:
						self._groups[l] = ll


	def on_modified(self, view):
		self._rescan(view)

	def on_activated(self, view):
		self._rescan(view)

	def on_selection_modified(self, view):
		# NOTE: can sel() return empty list?
		row, _ = view.rowcol(view.sel()[0].a)
		if row in self._groups:
			regs = []
			for roww in self._groups[row]:
				regs.append(self._regions[roww])
			view.add_regions('ifdef',regs,'comment','',sublime.HIDE_ON_MINIMAP)
		else:
			view.erase_regions('ifdef')
