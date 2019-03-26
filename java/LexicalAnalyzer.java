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

    public Pair<Vector<Pair<String, String>>, Vector<String>> Analyze() {
        tokenList = new Vector<Pair<String, String>>();
        errorList = new Vector<String>();
        myTokenMap mt = new myTokenMap();
        int tokenCounter = 0;

        try {
            Scanner sc = new Scanner(this.sourceFile);
            String content = "";
            while (sc.hasNextLine()) {
                content = content + sc.nextLine() + " * ";
            }

            // Pre-process raw string
            content = content.replaceAll(";", " ; ");
            content = content.replaceAll(":=", " := ");
            content = content.replaceAll("\\+", " + ");
            content = content.replaceAll("-", " - ");
            content = content.replaceAll("\\*", " * ");
            content = content.replaceAll("/", " / ");
            content = content.replaceAll(":[^=]", " : ");
            content = content.replaceAll("\\(", " ( ");
            content = content.replaceAll("\\)", " ) ");
            content = content.replaceAll("<[^=]", " < ");
            content = content.replaceAll(">[^=]", " > ");
            content = content.replaceAll("<=", " <= ");
            content = content.replaceAll(">=", " >= ");
            content = content.replaceAll(",", " , ");
            content = content.replaceAll("'", " ' ");
            content = content.replaceAll("\\.{2}", " .. ");
            content = content.replaceAll("\\([\\s]{1,}\\*", "(*");
            content = content.replaceAll("\\*[\\s]{1,}\\)", "*)");

            // System.out.println(content);

            StringTokenizer st = new StringTokenizer(content);

            int t;
            int columnCounter = 0;
            int rowCounter = 0;
            boolean isCommentValid = false;
            boolean isStringConstantOver = false;
            int isSingleQuote = 0;
            String chAndStr = "";
            String previousToken = "";

            while (st.hasMoreTokens()) {
                String currentToken = st.nextToken();
                if (currentToken.equals("*")) {
                    rowCounter++;
                    columnCounter = 0;
                    continue;
                }

                columnCounter += currentToken.length();

                if (currentToken.equals("(*")) {
                    isCommentValid = true;
                    continue;
                }

                if (currentToken.equals("*)")) {
                    isCommentValid = false;
                    continue;
                }

                if (isCommentValid == true) {
                    continue;
                }

                if (currentToken.equals("'")) {
                    if (isSingleQuote == 1) {
                        // System.out.println(chAndStr.length());
                        if (chAndStr.length() == 1) {
                            tokenList.add(new Pair<String, String>(chAndStr, "CCONST" + Integer.toString(++tokenCounter)));
                        } else {
                            if (chAndStr.length() > 10) {
                                errorList.add(new String("[ERROR]" + "[" + Integer.toString(rowCounter)
                                    + "," + Integer.toString(columnCounter) + "]: String contanst over the line boundary."));
                            }

                            tokenList.add(new Pair<String, String>(chAndStr, "SCONST" + Integer.toString(++tokenCounter)));
                        }

                        chAndStr = "";
                    }

                    isSingleQuote = 1 - isSingleQuote;
                    continue;
                }

                if (isSingleQuote == 1) {
                    chAndStr += currentToken;
                    continue;
                }

                if (currentToken.matches("^[0-9]+$") == true) {
                    tokenList.add(new Pair<String, String>(currentToken, "ICONST" + Integer.toString(++tokenCounter)));
                    continue;
                }

                String parsed = mt.get(currentToken);

                if (parsed != null) {
                    parsed = parsed.substring(0, parsed.length() - 6);
                    parsed += Integer.toString(tokenCounter++);
                    tokenList.add(new Pair<String, String>(currentToken, parsed));
                } else {
                    if (previousToken.equals("program")
                        || previousToken.equals("var")
                        || previousToken.equals(";")
                        || previousToken.equals("constant")
                        || previousToken.equals("begin")) {

                        tokenList.add(new Pair<String, String>(currentToken, "ID" + Integer.toString(++tokenCounter)));
                    }
                }

                previousToken = currentToken;
            }

            if (isCommentValid == true) {
                errorList.add(new String("[ERROR]: Comment are never terminated"));
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            // Success
        }

        return new Pair<Vector<Pair<String, String>>, Vector<String>>(tokenList, errorList);
    }

    public static void main(String[] args) {
        LexicalAnalyzer lAnalyzer = new LexicalAnalyzer(new File("sieve.pasc"));
        Pair<Vector<Pair<String, String>>, Vector<String>> returned = lAnalyzer.Analyze();
        Vector<Pair<String, String>> vecToken = returned.first;
        Vector<String> vecError = returned.second;

        try {
            BufferedWriter bw = new BufferedWriter(new FileWriter("out.txt"));
            for (Pair<String, String> p : vecToken) {
                bw.write(p + "\n");
            }
            bw.close();

            for (String str : vecError) {
                System.out.println(str);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
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
