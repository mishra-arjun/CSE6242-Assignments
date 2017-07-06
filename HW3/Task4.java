package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;


public class Task4 {

	public static class GraphMapper extends Mapper<Object, Text, Text, IntWritable>{

	private Text node = new Text();
    private final static IntWritable cnt = new IntWritable(1);	
    
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
      StringTokenizer line_split = new StringTokenizer(value.toString()); //The stringtokenizer (from wordcount) breaks the string into tokens over which we can iterate.
      while (line_split.hasMoreTokens()) {
        node.set(line_split.nextToken());
        context.write(node, cnt);
      }
    }
   }

    public static class GraphMapper1 extends Mapper<Object, Text, Text, IntWritable>{
    
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
      String [] line_split1 = value.toString().split("\t");
      context.write(new Text(line_split1[1]), new IntWritable(1));
      }
    }

    public static class GraphReducer extends Reducer<Text,IntWritable,Text,IntWritable> {
    private IntWritable result = new IntWritable();
    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
      int fin = 0;
      for (IntWritable x : values) {
      	fin += x.get();
      }
      result.set(fin);
      context.write(key, result);
      }
  	}

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    		Job job1 = Job.getInstance(conf, "Task4_Job1");
			job1.setJarByClass(Task4.class);
    		job1.setMapperClass(GraphMapper.class);
    		job1.setReducerClass(GraphReducer.class);
    		job1.setOutputKeyClass(Text.class);
    		job1.setOutputValueClass(IntWritable.class);
    		FileInputFormat.addInputPath(job1, new Path(args[0]));
    		FileOutputFormat.setOutputPath(job1, new Path("Temp_file"));
			
			boolean success = job1.waitForCompletion(true);
			if (success) {
			Job job2 = Job.getInstance(conf, "Task4_Job2");
				job2.setJarByClass(Task4.class);
	    		job2.setMapperClass(GraphMapper1.class);
	    		job2.setReducerClass(GraphReducer.class);
	    		job2.setOutputKeyClass(Text.class);
	    		job2.setOutputValueClass(IntWritable.class);
	    		FileInputFormat.addInputPath(job2, new Path("Temp_file"));
	    		FileOutputFormat.setOutputPath(job2, new Path(args[1]));
	    		System.exit(job2.waitForCompletion(true) ? 0 : 1);
	    	}	
  }
}
