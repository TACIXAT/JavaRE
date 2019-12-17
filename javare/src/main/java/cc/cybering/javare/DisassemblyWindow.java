package cc.cybering.javare;

import jexer.TApplication;
import jexer.TWindow;
import jexer.TList;
import jexer.event.TResizeEvent;
import java.util.List;


public class DisassemblyWindow extends TWindow {
	protected TList instructionList;

	public DisassemblyWindow(final TApplication app, String title, int width, int height, List<String> disassembly) 
	{
		super(app, title, width, height);
        this.instructionList = addList(disassembly, 0, 0, width-2, height-2);		
    }

	@Override
	public void onResize​(TResizeEvent event) {
		this.instructionList.setWidth(event.getWidth()-2);
		this.instructionList.setHeight(event.getHeight()-2);
        this.instructionList.reflowData();
	}    	
}