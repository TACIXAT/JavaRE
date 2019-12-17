package cc.cybering.javare;

import org.apache.bcel.classfile.ClassParser;
import org.apache.bcel.classfile.JavaClass;
import org.apache.bcel.classfile.Method;
import org.apache.bcel.classfile.ConstantPool;
import org.apache.bcel.classfile.Utility;
import org.apache.bcel.util.ByteSequence;
import org.apache.bcel.generic.InstructionList;
import org.apache.bcel.generic.InstructionHandle;
import jexer.TApplication;
import jexer.TWindow;
import jexer.TAction;
import jexer.TList;
import jexer.TWidget;
import jexer.event.TResizeEvent;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.jar.JarFile;
import java.util.jar.JarEntry;
import java.util.Enumeration;

public class App 
{
    public static void main( String[] args ) throws Exception
    {
    	if (args.length < 1) {
    		System.out.println("please provide a class file");
    		return;
    	}

    	// JarFile jarFile = new JarFile(args[0]);
    	// Enumeration<JarEntry> entries = jarFile.entries();
    	// while (entries.hasMoreElements()) {
    	// 	JarEntry jarEntry = entries.nextElement();
    	// 	System.out.println(jarEntry.getName());
    	// 	// jarFile.getInputStream(jarEntry);
    	// }

        ClassParser classParser = new ClassParser(args[0]);
    	JavaClass javaClass = classParser.parse();
    	ConstantPool shadowPool = javaClass.getConstantPool().copy();

        final TApplication app = new TApplication(
        	TApplication.BackendType.XTERM);
        app.addFileMenu();
        app.addWindowMenu();
        FunctionWindow window = new FunctionWindow(
        	app, javaClass.getClassName(), 10, 10, getMethodList(javaClass), Arrays.asList(javaClass.getMethods()), shadowPool);
        app.run();
    }

    static List<String> getMethodList(JavaClass javaClass) {
    	Method[] methods = javaClass.getMethods();
        List<String> methodList = new ArrayList<String>();
        for (Method method : methods) {
        	methodList.add(method.getName());
        }

        return methodList;
    }

	// static void dumpMethods(JavaClass javaClass) {
	// 	Method[] methods = javaClass.getMethods();
	// 	for (Method method : methods) {
	// 		System.out.println("==== " + method.getName());
	// 		InstructionList instructionList = new InstructionList(method.getCode().getCode());
	// 		List<String> disassembly = getDisassembly(method.getCode().getCode(), javaClass.getConstantPool());
	// 		int idx = 0;
	// 		for (InstructionHandle instruction : instructionList) {
	// 			System.out.println(instruction);
	// 			System.out.println(disassembly[idx]);
	// 			idx++;
	// 		}
	// 	}
	// }

	static void rename(ConstantPool constantPool, int index, String name) {

	}

	static void getBasicBlocks() {

	}
}
