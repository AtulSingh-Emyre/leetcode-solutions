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
    public ListNode deleteMiddle(ListNode head) {
        ListNode root = head;
        int l = 0;
        while (root!=null) {
            l++;
            root = root.next;
        }
        if(l==1) return null;
        ListNode prev = null;
        ListNode next = head;
        int idx = 0;
        while(true) {
            if(idx == l/2) {
                prev.next = next.next;
                break;
            }
            else {
                prev = next;
                next = next.next;
            }
            idx++;
        }
        return head;
    }
}