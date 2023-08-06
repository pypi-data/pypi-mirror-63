#############################################
##   Filename: CSHIO.py
##
##    Copyright (C) 2011 Marcus C. Newton
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
## Contact: Bonsu.Devel@gmail.com
#############################################
import wx
import sys
import os
import numpy
from .wrap import WrapArray
from .loadarray import NewArray
def CSHIO\
	(
		self,
		beta,
		startiter,
		numiter,
		cs_p,
		cs_epsilon,
		cs_epsilon_min,
		cs_d,
		cs_eta,
		relax
	):
	def updatereal():
		wx.CallAfter(self.ancestor.GetPage(1).UpdateReal,)
	def updaterecip():
		wx.CallAfter(self.ancestor.GetPage(1).UpdateRecip,)
	def updatelog():
		try:
			n = self.citer_flow[0]
			res = self.ancestor.GetPage(0).residual[n]
			string = "Iteration: %06d, Residual: %1.9f, Epsilon: %1.6e" %(n,res,epsilon[0])
			self.ancestor.GetPage(0).queue_info.put(string)
		except:
			pass
	seqdata = self.seqdata
	expdata = self.expdata
	support = self.support
	mask = self.mask
	residual = self.residual
	citer_flow = self.citer_flow
	visual_amp_real = self.visual_amp_real
	visual_amp_recip = self.visual_amp_recip
	visual_phase_real = self.visual_phase_real
	visual_phase_recip = self.visual_phase_recip
	try:
		rho_m1 = NewArray(self, *seqdata.shape)
		rho_m2 = NewArray(self, *seqdata.shape)
		elp = NewArray(self, *seqdata.shape)
	except:
		return
	epsilon = numpy.zeros((2),dtype=numpy.double)
	epsilon[0] = cs_epsilon
	epsilon[1] = cs_epsilon_min
	nn=numpy.asarray( seqdata.shape, numpy.int32 )
	ndim=int(seqdata.ndim)
	from ..lib.prfftw import cshio
	cshio(seqdata,expdata,support, mask,\
	beta,startiter,numiter,ndim,\
	cs_p,epsilon,cs_d,cs_eta,relax,\
	rho_m1,rho_m2,elp,nn,residual,citer_flow,\
	visual_amp_real,visual_phase_real,visual_amp_recip,visual_phase_recip,\
	updatereal,updaterecip, updatelog)
