import java.util.*;
public class MyCalendar {
	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		ArrayList<Integer> arr1=new ArrayList<Integer>();
		Random r1=new Random();
		MyTimer t1=new MyTimer();
		for(int i=0; i<1000000; i++)
			arr1.add(r1.nextInt());
		t1.printTime("test Array");
		System.out.println("size="+arr1.size());
		MyTimer t2=new MyTimer();
		for(int i=0; i<10000; i++)
			arr1.indexOf(r1.nextInt());
		t2.printTime("Find Array");
		TreeSet<Integer> set1=new TreeSet<Integer>();
		MyTimer t3=new MyTimer();
		for(int i=0; i<1000000; i++)
			set1.add(i);
		t3.printTime("test TreeSet");
		System.out.println("size="+set1.size());
		MyTimer t4=new MyTimer();
		for(int i=0; i<10000; i++)
			set1.contains(r1.nextInt());
		t4.printTime("Find TreeSet");
		LinkedList<Integer> l1=new LinkedList<Integer>();
		MyTimer t5=new MyTimer();
		for(int i=0; i<1000000; i++)
			l1.add(r1.nextInt());
		t5.printTime("test List");
		System.out.println("size="+l1.size());
		MyTimer t6=new MyTimer();
		for(int i=0; i<10000; i++)
			l1.indexOf(r1.nextInt());
		t6.printTime("Find List");
		HashSet<Integer> hash1=new HashSet<Integer>();
		MyTimer t7=new MyTimer();
		for(int i=0; i<1000000; i++)
			hash1.add(i);
		t7.printTime("test HashSet");
		System.out.println("size="+hash1.size());
		MyTimer t8=new MyTimer();
		for(int i=0; i<10000; i++)
			hash1.contains(r1.nextInt());
		t8.printTime("Find HashSet");

	}

}
