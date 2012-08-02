package xmipp.ij.commons;

import java.awt.event.MouseEvent;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;
import javax.swing.SwingUtilities;

import xmipp.ij.commons.Tool;
import ij.IJ;
import ij.ImagePlus;
import ij.gui.ImageCanvas;

public class XmippImageCanvas extends ImageCanvas implements MouseWheelListener
{

	public Tool getTool()
	{

		if (IJ.getInstance() == null)
			return Tool.PICKER;
		return Tool.getTool(IJ.getToolName());
	}
	
	

	public XmippImageCanvas(ImagePlus imp)
	{
		super(imp);
		addMouseWheelListener(this);
	}

	public void mousePressed(MouseEvent e)
	{
		if (getTool() == Tool.IMAGEJ)
		{
			super.mousePressed(e);
			return;
		}

		int x = super.offScreenX(e.getX());
		int y = super.offScreenY(e.getY());

		if (isDragImage(e))
		{
			setupScroll(x, y);
			return;
		}

	}
	
	protected boolean isDragImage(MouseEvent e)
	{
		return SwingUtilities.isRightMouseButton(e)  || (SwingUtilities.isLeftMouseButton(e) && e.isControlDown());
	}

	public void mouseDragged(MouseEvent e)
	{

		if (getTool() == Tool.IMAGEJ)
		{
			super.mouseDragged(e);
			return;
		}
		if (isDragImage(e))
		{
			scroll(e.getX(), e.getY());
			return;
		}
	}
	
	public void mouseReleased(MouseEvent e)
	{
		if (getTool() == Tool.IMAGEJ)//do nothing for ImageJ tool is mine is selected
		{
			super.mouseReleased(e);
			return;
		}
		
	}

	@Override
	public void mouseWheelMoved(MouseWheelEvent e)
	{
		if(!e.isShiftDown())
			return;
		int x = e.getX();
		int y = e.getY();

		int rotation = e.getWheelRotation();
		if (rotation < 0)
			zoomIn(x, y);
		else
			zoomOut(x, y);
		if (getMagnification() <= 1.0)
			imp.repaintWindow();

	}
	
	public void mouseMoved(MouseEvent e)
	{


		if (getTool() == Tool.IMAGEJ)
			super.mouseMoved(e);
		int x = offScreenX(e.getX());
		int y = offScreenY(e.getY());
		imp.mouseMoved(x, y);
		imp.updateStatusbarValue();
	}


}
