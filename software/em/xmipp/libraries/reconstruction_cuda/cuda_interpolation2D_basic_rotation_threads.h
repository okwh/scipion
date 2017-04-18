/***************************************************************************
 * Authors:     Amaya Jimenez (ajimenez@cnb.csic.es)
 *
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
 *  e-mail address 'xmipp@cnb.csic.es'
 ***************************************************************************/

#ifndef CUDA_BASIC_INTERPOLATION2D_TH
#define CUDA_BASIC_INTERPOLATION2D_TH

#include "cuda_basic_math.h"


__global__ void
rotate_kernel_normalized_2D_threads(float *output, size_t Xdim, size_t Ydim, double *angle, cudaTextureObject_t my_tex, int thIdx)
{

    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;

    if(x==0 && y==0){
    	printf("Dimensiones del hilo %i : %i x %i \n", thIdx, (int)Xdim, (int)Ydim);
    }

    //for (int i=0; i<5; i++){

    	/*size_t Xdim=Xdimv[0];
    	size_t Ydim=Ydimv[0];
    	double *angle = &anglev[offset_angle];*/


    if(x>=Xdim || y>=Ydim){
    	//continue;
    	return;
    }

    // Transform coordinates
    float u = x / (float)Xdim;
    float v = y / (float)Ydim;

    u = (Xdim%2==0) ? u-0.5 : u-(trunc((float)(Xdim/2.))/Xdim);
    v = (Ydim%2==0) ? v-0.5 : v-(trunc((float)(Ydim/2.))/Ydim);
    //u -= 0.5f; //- (float(0.5)/(float)Xdim);
    //v -= 0.5f; //+ (float(0.5)/(float)Ydim);

    float desp_u = ((float)angle[2]/(float)Xdim);
    float desp_v = ((float)angle[5]/(float)Ydim);

    //float tu = u * (float)angle[0] + v * (float)angle[1] + desp_u + 0.5f + (float(0.5)/(float)Xdim);
    //float tv = u * (float)angle[3] + v * (float)angle[4] + desp_v + 0.5f + (float(0.5)/(float)Ydim);
    float tu = u * (float)angle[0] + v * (float)angle[1] + desp_u + (float(0.5)/(float)Xdim);
    float tv = u * (float)angle[3] + v * (float)angle[4] + desp_v + (float(0.5)/(float)Ydim);
    tu = (Xdim%2==0) ? tu+0.5 : tu+(trunc((float)(Xdim/2.))/Xdim);
    tv = (Ydim%2==0) ? tv+0.5 : tv+(trunc((float)(Ydim/2.))/Ydim);

    // Read from texture and write to global memory
    if(x==0 && y==0){
    	printf("Llamada a la textura del hilo %i \n", thIdx);
    }
   	output[(y * Xdim + x)] = tex2D<float>(my_tex, tu, tv);


   	//offset=offset+(Xdim*Ydim);
   	//offset_angle=offset_angle+9;

    //}

}

#endif
