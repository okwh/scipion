/***************************************************************************
 *
 * Authors:     Debora Gil
 *              Roberto Marabini
 *
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
 *  e-mail address 'xmipp@cnb.uam.es'
 ***************************************************************************/
/*****************************************************************************/
/* Experimental Lattice                                                      */
/*****************************************************************************/

#ifndef _XMIPP_CCLATTICE_IO_HH
#define _XMIPP_CCLATTICE_IO_HH

#include <vector>

#include <data/funcs.h>
#include <data/matrix2d.h>
#include <data/geometry.h>

/**@defgroup ccLattice Correlation Lattice I/O
   @ingroup InterfaceLibrary */
//@{
/** Correlation Lattice I/O.
    This is a class to read/write Corelation files as produced by the MRC's program
    quadserach.
    @code
         1
         2
         3
         4
         5
         2000        2000        1000        1000   58.19258       25.64419
    25.15103      -56.71311            -120         120        -120         120
    56789
     0.000     0.000            0.00
     0.000     0.000            0.00
     0.000     0.000            0.00
     0.000     0.000            0.00
     0.000     0.000            0.00
     0.000     0.000            0.00
     0.000     0.000            0.00
     0.000     0.000            0.00
    @endcode

    Each line after the fifth gives de position of a correlation maxima
    */


/////////////////////////////// DATA TYPES //////////////////////////////

class CCLattice_IO
{


public:

    /* Lattice Param. */
    /** Crystal  dimensions */
    int dim[2];
    /** Search origing in MRC coordinates */
    double O[2];
    /** a vector */
    Matrix1D <double> a;
    /** b vector */
    Matrix1D <double> b;
    /** Index Ranges for a vector **/
    int max_i, min_i;
    /** Index Ranges for b vector **/
    int max_j, min_j;
    /** Croscorrelation maximun */
    double cc_max;


    /** Vectors to store optimal X and Y position plus croos correlation  peaks */
    //Peaks Coord.
    //Correlation Peaks
    vector <double> MRC_Xcoord;
    vector <double> MRC_Ycoord;
    vector <int> MRC_Xindex;
    vector <int> MRC_Yindex;

    //Cross Correlation
    vector <double> MRC_CCcoheficiente;


////////////////////////////////  FUNCTIONS //////////////////////////

public:

////////////////////////////  Constructors
    CCLattice_IO();

//////////////////////////// I/O functions

    /** Read a cor file generated by the MRC program quadserach.
        */
    void read(const FileName &fn);
    /** Write a cor file as  the ones generated by the MRC program quadserach.
        */
    void write(const FileName &fn);

////////////////////////////

    /* Show parameters --------------------------------------------------------- */
    friend ostream & operator << (ostream &o, const CCLattice_IO &prm)
    {
        o << "astar vector              :   " << prm.a << endl
        << "bstar vector              :   " << prm.b << endl
        << "Cristal_dim               :   " << prm.dim[0] << " "
        << prm.dim[1] << endl
        << "Cristal_Search_Origen     :   " << prm.O[0] << " "
        << prm.O[1] << endl
        ;

        return o;
    }
};
//@}

#endif
