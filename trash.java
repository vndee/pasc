while ((t = st.nextToken()) != StreamTokenizer.TT_EOF) {
    switch (t) {
        case StreamTokenizer.TT_WORD:
            if (isCommentValid == true)
                break;

            String currentToken = st.sval;
            String parsed = mt.get(currentToken);

            if (parsed != null) {
                parsed = parsed.substring(0, parsed.length() - 6);
                parsed += Integer.toString(tokenCounter++);
                tokenList.add(new Pair<String, String>(currentToken, parsed));

                // System.out.println(parsed);

            }

            break;

        case StreamTokenizer.TT_NUMBER:
            break;

        case StreamTokenizer.TT_EOL:
            break;

        case StreamTokenizer.TT_EOF:
            break;

        default:
    }
}
