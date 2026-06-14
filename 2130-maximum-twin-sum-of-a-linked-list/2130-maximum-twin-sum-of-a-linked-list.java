/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public int pairSum(ListNode head) {
        Stack<Integer> stack = new Stack<>();
        int n = 1;
        ListNode root = head;
        while(root.next!=null) {
            root = root.next;
            n++;
        }
        int idx = 0;
        int result = Integer.MIN_VALUE;
        root = head;
        while(root!=null) {
            if(idx>=0 && idx<=((n/2)-1)) stack.add(root.val);
            else {
                int curr = stack.pop();
                result = Math.max(result, curr+ root.val);
            }
            root = root.next;
            idx++;
        }
        return result;
    }
}