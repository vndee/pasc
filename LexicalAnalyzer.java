import java.io.*;
import java.util.*;

public class LexicalAnalyzer {
    private File sourceFile;    // Source file
    private Vector<String> errorList;

    private class Pair<X, Y> {
        /**
         * Pair contains two value in one object
         */

        public X first;
        public Y second;

        /**
         * Default constuctor
         */
        public Pair() {}

        /**
         * Specific constructor with specified value
         * @param first: X (Generic data type)
         * @param second: Y (Generic data type)
         */
        public Pair(X first, Y second) {
            this.first = first;
            this.second = second;
        }

        @Override
        /**
         * equals: Check whether an object is "equal to" current object or not
         * @param obj: Object
         * @return boolean
         */
        public boolean equals(Object obj) {
            if (this == obj)
                return true;

            if (obj == null || getClass() != obj.getClass())
                return false;

            Pair<?, ?> pair = (Pair<?, ?>) obj;

            return first.equals(pair.first) && second.equals(pair.second);
        }

        @Override
        /**
         * toString: Convert an pair object to string
         * @return String
         */
        public String toString() {
            return "(" + first + ", " + second + ")";
        }
    }

    private Vector<Pair<String, String>> tokenList;

    /**
     * Default constructor
     */
    public LexicalAnalyzer() {}

    /**
     * LexicalAnalyzer specific constructor
     * @param sourceFile: File contains code need to be analyzed.
     * @return void
     */
    public LexicalAnalyzer(File sourceFile) {
        this.sourceFile = sourceFile;
    }

    private void TokenAnalyzer() {

    }

    public void print(String str) {
        System.out.print(str);
    }

    public void Analyze() {
        tokenList = new Vector<Pair<String, String>>();
        errorList = new Vector<String>();
        myTokenMap mt = new myTokenMap();
        int tokenCounter = 0;

        try {
            String content = new Scanner(this.sourceFile).useDelimiter("\\Z").next();
            content = content.replaceAll("[a-zA-Z0-9];", ";");
            System.out.println(content);
            StringTokenizer st = new StringTokenizer(content);


            int t;
            boolean isCommentValid = false;


            if (isCommentValid == true) {
                errorList.add(new String("[ERROR]: Comment are never terminated"));
            }

            for(Pair<String, String> i: tokenList){
                System.out.println(i);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            // Success
        }
    }

    public static void main(String[] args) {
        LexicalAnalyzer lAnalyzer = new LexicalAnalyzer(new File("sieve.pasc"));
        lAnalyzer.Analyze();
    }
}

class myTokenMap{
    public Map<String, String> map = new HashMap<String, String>();

    public myTokenMap(){
        map.put("end  of file", "EOFnumber");
        map.put(";", "SEMInumber");
        map.put(":", "COLONnumber");
        map.put(",", "COMMMAnumber");
        map.put(".", "DOTnumber");
        map.put("(", "LPARENnumber");
        map.put(")", "RPARENnumber");
        map.put("<", "LTnumber");
        map.put(">", "GTnumber");
        map.put("=", "EQnumber");
        map.put("-", "MINUSnumber");
        map.put("+", "PLUSnumber");
        map.put("*", "TIMESnumber");
        map.put("..", "DOTDOTnumber");
        map.put(":=", "COLEQnumber");
        map.put("<=", "LEnumbernumber");
        map.put(">=", "GEnumber");
        map.put("<>", "NEnumber");
        map.put("identifier", "IDnumber");
        map.put("integer constant", "ICONSTnumber");
        map.put("char constant", "CCONSTnumber");
        map.put("string constant", "SCONSTnumber");
        map.put("and", "ANDnumber");
        map.put("array", "ARRAYnumber");
        map.put("begin", "BEGINnumber");
        map.put("constant", "CONSTnumber");
        map.put("div", "DIVnumber");
        map.put("downto", "DOWNTOnumber");
        map.put("else", "ELSEnumber");
        map.put("elsif", "ELSIFnumber");
        map.put("end", "ENDnumber");
        map.put("endif", "ENDIFnumber");
        map.put("endloop", "ENDLOOPnumber");
        map.put("endrec", "ENDRECnumber");
        map.put("exit", "EXITnumber");
        map.put("for", "FORnumber");
        map.put("forward", "FORWARDnumber");
        map.put("function", "FUNCTIONnumber");
        map.put("if", "IFnumber");
        map.put("is", "ISnumber");
        map.put("loop", "LOOPnumber");
        map.put("not", "NOTnumber");
        map.put("of", "OFnumber");
        map.put("or", "ORnumber");
        map.put("procedure", "PROCEDUREnumber");
        map.put("program", "PROGRAMnumber");
        map.put("record", "RECORDnumber");
        map.put("repeat", "REPEATnumber");
        map.put("return", "RETURNnumber");
        map.put("then", "THENnumber");
        map.put("to", "TOnumber");
        map.put("type", "TYPEnumber");
        map.put("until", "UNTILnumber");
        map.put("var", "VARnumber");
        map.put("while", "WHILEnumber");
    }

    public String get(String key){
        return this.map.get(key);
    }

}
