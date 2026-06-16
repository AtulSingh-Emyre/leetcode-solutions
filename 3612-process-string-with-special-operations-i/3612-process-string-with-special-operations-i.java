

class Solution {
    public String processStr(String s) {
        StringBuilder sb = new StringBuilder("");
        char[] carr = s.toCharArray();
        for(char c : carr) {
            if (c == '*' && sb.length()==0) {
                continue;
            }
            else if (c == '*' && sb.length()>=1) {
                sb.deleteCharAt(sb.length() - 1);
            }  
            else if (c == '#') {
                sb.append(sb);
            }
            else if (c == '%') {
                sb.reverse();
            } else sb.append(c);
                // System.out.println(sb);
        }
        return sb.toString();
    }
}