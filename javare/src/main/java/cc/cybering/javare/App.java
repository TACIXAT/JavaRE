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

    	/*
			Tree style display?
			Class -> Vars / Functions

    		Handle Jar ==
			Iterate jar
			Replace path / -> .
			Save map of full class name -> jarentry
			Display list of classes
			Open class
			Use what we currently have from there
			
			Renaming ==
			Map of old -> new name
			Apply replacements to constant pool
			Save position
			Recalculate disassembly
			Restore position
			Class replacements and jar level replacements

			Goto addr ==
			Binary search for string prefix?
			Probably just brute force initially
			Maybe create a map of addr -> line
			Set position

			Comment ==
			Map function:line -> comment

			Find Definition ==
			Open class
			Find function or variable

			Auto Rename All ==
			Iterate all classes
			Rename functions -> FuncTypeA
			Rename class vars -> ClassVarTypeA
			Rename locals?
    	*/

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
