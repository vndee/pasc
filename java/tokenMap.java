public class tokenMap{
    public static Map<String, String> map = new Stream.of(new Object[][]{
        {"end  of file", "EOFnumber"},
        {";", "SEMInumber"}
    }).collect(Collectors.toMap(p -> (String)p[0], p -> (String)p[1]));

}