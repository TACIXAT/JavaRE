package cc.cybering.javare;

import org.apache.bcel.classfile.Method;
import org.apache.bcel.classfile.ConstantPool;
import jexer.TApplication;
import jexer.TWindow;
import jexer.TAction;
import jexer.TList;
import jexer.event.TResizeEvent;
import java.util.List;
import org.apache.bcel.classfile.Utility;
import org.apache.bcel.util.ByteSequence;
import java.util.Arrays;


public class FunctionWindow extends TWindow {
	protected TList functionList;
	protected ConstantPool shadowPool;

	public FunctionWindow(
		final TApplication app, 
		String title, 
		final int width, 
		final int height,
		List<String> nameList, 
		final List<Method> methodList, 
		ConstantPool shadowPool) 
	{
		super(app, title, width, height);
		this.shadowPool = shadowPool;

		TAction functionSelectAction = new TAction() {
            public void DO() {
            	TList fnList = (TList)source;
                
                Method method = methodList.get(fnList.getSelectedIndex());
                List<String> disassembly = getDisassembly(method.getCode().getCode(), FunctionWindow.this.shadowPool);
                
                TWindow disasWindow = new DisassemblyWindow(app, fnList.getSelected(), app.getDesktop().getWidth(), app.getDesktop().getHeight(), disassembly);
            }
        };

		this.functionList = addList(
        	nameList, 0, 0, getWidth()-2, 
        	getHeight()-2, functionSelectAction);
    }

	@Override
	public void onResize​(TResizeEvent event) {
		this.functionList.setWidth(event.getWidth());
		this.functionList.setHeight(event.getHeight());
	}    	

	List<String> getDisassembly(final byte[] code, final ConstantPool constantPool) {
	 	final StringBuilder buf = new StringBuilder(code.length * 20);
		try (ByteSequence stream = new ByteSequence(code)) {
            for (int i = 0; stream.available() > 0; i++) {
                final String indices = Utility.fillup(stream.getIndex() + ":", 6, true, ' ');
                buf.append(indices).append(Utility.codeToString(stream, constantPool, false).replace("\t", " ")).append('\n');
            }
        } catch (final Exception e) {
            System.out.println(e);
        }
        return Arrays.asList(buf.toString().split("\n"));
	}
}