/***************************************************************************
 *
 * Authors:    Carlos Oscar Sanchez Sorzano coss@cnb.csic.es
 *             David Strelak david.strelak@gmail.com
 * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
 * 02111-1307  USA
 *
 *  All comments concerning this program package may be sent to the
 *  e-mail address 'xmipp@cnb.csic.es'
 ***************************************************************************/

#ifndef _PROG_MOVIE_ALIGNMENT_CORRELATION
#define _PROG_MOVIE_ALIGNMENT_CORRELATION

#include "data/filters.h"
#include "data/xmipp_fftw.h"
#include "reconstruction/movie_alignment_correlation_base.h"


/** Movie alignment correlation Parameters. */
class ProgMovieAlignmentCorrelation: public AProgMovieAlignmentCorrelation
{
protected:
	// Fourier transforms of the input images
	std::vector< MultidimArray<std::complex<double> > * > frameFourier;

protected:
	void loadData(const MetaData& movie, const Image<double>& dark,
			const Image<double>& gain,
			double targetOccupancy,
			const MultidimArray<double>& lpf);

	void computeShifts(size_t N, const Matrix1D<double>& bX,
			const Matrix1D<double>& bY, const Matrix2D<double>& A);
};

#endif
