package cc.cybering.javare;

import org.apache.bcel.classfile.ClassParser;
import org.apache.bcel.classfile.JavaClass;
import org.apache.bcel.classfile.Method;
import org.apache.bcel.classfile.ConstantPool;
import org.apache.bcel.classfile.Utility;
import org.apache.bcel.util.ByteSequence;
import org.apache.bcel.generic.InstructionList;
import org.apache.bcel.generic.InstructionHandle;

public class App 
{
    public static void main( String[] args )
    {
    	if (args.length < 1) {
    		System.out.println("please provide a class file");
    		return;
    	}

        ClassParser classParser = new ClassParser(args[0]);
        try {
        	JavaClass javaClass = classParser.parse();
        	System.out.println(javaClass);
        	dumpMethods(javaClass);
        } catch(Exception e) {
        	System.out.println(e);
        }
    }

	static void dumpMethods(JavaClass javaClass) {
		Method[] methods = javaClass.getMethods();
		for (Method method : methods) {
			System.out.println("==== " + method.getName());
			InstructionList instructionList = new InstructionList(method.getCode().getCode());
			String[] disassembly = getDisassembly(method.getCode().getCode(), javaClass.getConstantPool());
			int idx = 0;
			for (InstructionHandle instruction : instructionList) {
				System.out.println(instruction);
				System.out.println(disassembly[idx]);
				idx++;
			}
		}
	}

	static String[] getDisassembly(final byte[] code, final ConstantPool constantPool) {
	 	final StringBuilder buf = new StringBuilder(code.length * 20);
		try (ByteSequence stream = new ByteSequence(code)) {
            for (int i = 0; stream.available() > 0; i++) {
                final String indices = Utility.fillup(stream.getIndex() + ":", 6, true, ' ');
                buf.append(indices).append(Utility.codeToString(stream, constantPool, false)).append('\n');
            }
        } catch (final Exception e) {
            System.out.println(e);
        }
        return buf.toString().split("\n");
	}

	static rename(ConstantPool constantPool, int index, String name) {
		
	}
}
